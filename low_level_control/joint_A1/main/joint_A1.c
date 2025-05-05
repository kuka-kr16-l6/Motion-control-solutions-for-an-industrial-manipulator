#include <stdio.h>
#include "driver/uart.h"
#include <driver/gpio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <string.h>
#include <esp_log.h>

#define TAG "Joint_A1"

// GPIO Definitions
#define BUILT_IN_LED 2
#define UART_TXD_PIN 17
#define UART_RXD_PIN 16
#define MOTOR_PULSE_PIN 13
#define MOTOR_DIRECTION_PIN 14
#define MOTOR_ENABLE_PIN 27
#define RTC_PIN 12

// Motor Constants
#define PULSES_PER_DEGREE 700
#define MIN_HALF_PERIOD_US 8  // Maximum speed corresponds to shortest half-period
#define MAX_QUEUE_SIZE 100
#define MOTOR_ADDRESS 1

// UART Configuration
#define UART_PORT UART_NUM_1
#define UART_BUFFER_SIZE 1024 * 2
#define UART_QUEUE_SIZE 50

typedef struct {
    float target_angle_deg;
    bool direction_cw;
    uint8_t torque_limit;
    uint8_t half_period_us;
} motor_params_t;

static QueueHandle_t uart_event_queue;
static QueueHandle_t motor_params_queue = NULL;

// Global state variables
static int movement_count = 0;
static float current_angle_deg = 0.00f;

void uart_init(void);
void gpio_init(void);

// Task handling incoming UART data
void receive_event_task(void *pvParameter)
{
    uart_event_t event;
    uint8_t rx_buffer[5];
    gpio_set_level(RTC_PIN, 0);
    
    while (true) {
        if (xQueueReceive(uart_event_queue, &event, pdMS_TO_TICKS(50)) == pdTRUE) {
            switch (event.type) {
                case UART_DATA: {
                    int len = uart_read_bytes(UART_PORT, rx_buffer, event.size, pdMS_TO_TICKS(100));
                    
                    if (len > 0 && rx_buffer[0] == MOTOR_ADDRESS) { // Check for motor ID match
                        motor_params_t params = {
                            .target_angle_deg = ((rx_buffer[1] << 8) | rx_buffer[2]) / 100.0f,
                            .direction_cw = rx_buffer[3] & 0x01,
                            .half_period_us = rx_buffer[4],
                            .torque_limit = 255
                        };

                        // Enforce minimum speed limit
                        if (params.half_period_us < MIN_HALF_PERIOD_US) {
                            params.half_period_us = MIN_HALF_PERIOD_US;
                        }

                        ESP_LOGD(TAG, "Received command: %.2f°, %s, %dμs",
                            params.target_angle_deg,
                            params.direction_cw ? "CW" : "CCW",
                            params.half_period_us);

                        if (xQueueSend(motor_params_queue, &params, pdMS_TO_TICKS(100)) != pdTRUE) {
                            ESP_LOGE(TAG, "Failed to enqueue motor parameters");
                        }
                    }
                    memset(rx_buffer,0,sizeof(rx_buffer));
                    break;
                }
                case UART_FRAME_ERR:
                    ESP_LOGE(TAG, "UART framing error");
                    break;
                default:
                    break;
            }
        }
    }
}

// Task handling motor movements
void motor_control_task(void *pvParameter)
{
    motor_params_t params;
    const TickType_t idle_delay = pdMS_TO_TICKS(100);
    
    while (true) {
        if (xQueueReceive(motor_params_queue, &params, pdMS_TO_TICKS(50)) == pdTRUE) {
            movement_count++;
            
            // Configure motor direction
            gpio_set_level(MOTOR_DIRECTION_PIN, params.direction_cw);
            
            // Calculate required pulses
            int pulse_count = (int)(params.target_angle_deg * PULSES_PER_DEGREE);
            
            // Generate pulses
            for (int i = 0; i < pulse_count; i++) {
                gpio_set_level(MOTOR_PULSE_PIN, 1);
                esp_rom_delay_us(params.half_period_us);
                gpio_set_level(MOTOR_PULSE_PIN, 0);
                esp_rom_delay_us(params.half_period_us);
            }
            
            // Update position tracking
            current_angle_deg += params.direction_cw ? params.target_angle_deg : -params.target_angle_deg;
            
            ESP_LOGI(TAG, "Moved %.3f° %s, %d pulses", 
                   params.target_angle_deg,
                   params.direction_cw ? "CW" : "CCW",
                   pulse_count);
        } else {
            ESP_LOGD(TAG, "Current angle: %.2f°, Movements: %d", current_angle_deg, movement_count);
            vTaskDelay(idle_delay);
        }
    }
}

void app_main(void)
{
    // Initialize peripherals
    gpio_init();
    uart_init();
    
    // Create communication queue
    motor_params_queue = xQueueCreate(MAX_QUEUE_SIZE, sizeof(motor_params_t));
    if (!motor_params_queue) {
        ESP_LOGE(TAG, "Failed to create motor parameters queue");
        return;
    }
    
    // Start tasks
    xTaskCreatePinnedToCore(receive_event_task, "UART Receiver", 4096, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(motor_control_task, "Motor Controller", 4096, NULL, 5, NULL, 0);
    
    ESP_LOGI(TAG, "System initialized successfully");
}

void uart_init(void)
{
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT
    };
    
    ESP_ERROR_CHECK(uart_param_config(UART_PORT, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_PORT, UART_TXD_PIN, UART_RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(UART_PORT, UART_BUFFER_SIZE * 2, UART_BUFFER_SIZE * 2, UART_QUEUE_SIZE, &uart_event_queue, 0));
}

void gpio_init(void)
{
    // Configure motor control pins
    gpio_set_direction(MOTOR_PULSE_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(MOTOR_DIRECTION_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(MOTOR_ENABLE_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(BUILT_IN_LED, GPIO_MODE_OUTPUT);
    
    // Configure RS485 direction control
    gpio_set_direction(RTC_PIN, GPIO_MODE_OUTPUT);
    
    // Initial pin states
    gpio_set_level(MOTOR_ENABLE_PIN, 1);  // Enable motor driver
    gpio_set_level(BUILT_IN_LED, 0);      // LED off
    gpio_set_level(RTC_PIN, 0);           // Default UART receive mode
    
    // Allow time for motor driver initialization
    vTaskDelay(pdMS_TO_TICKS(2000));
}
