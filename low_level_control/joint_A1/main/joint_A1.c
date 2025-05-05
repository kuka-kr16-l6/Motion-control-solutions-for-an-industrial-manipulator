#include <stdio.h>
#include "driver/uart.h"
#include <driver/gpio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/idf_additions.h>
#include <string.h>
#include <esp_log.h>

#define TAG  "Joint_A1"

// GPIO Definitions
#define BUILT_IN_LED 2
#define UART_TXD2_PIN 17
#define UART_RXD2_PIN 16
#define UART_TXD0_PIN 1
#define UART_RXD0_PIN 3
#define RTC_PIN 12
#define MOTOR_PULSE_PIN 13
#define MOTOR_SIGN_PIN 14
#define MOTOR_SERVO_ON 27

// Motor Constants
#define PULSE_PER_DEGREE  700
#define MIN_HALF_PERIOD_US 10
#define MAX_QUEUE_SIZE 100

// UART Configuration
#define MOTOR_ADDRESS 1
#define UART_QUEUE_SIZE 100

typedef struct {
    float target_angle_deg;    
    bool direction;         
    uint8_t torque_limit;       
    uint8_t half_period_us;     
} motor_params_t;


QueueHandle_t uart_event_queue;
QueueHandle_t motor_params_queue = NULL;

static float current_angle_deg = 0.00f;

void uart_init(void);
void gpio_init(void);

// Task handling incoming UART data
void receive_event_task(void *pvParameter)
{
    uart_event_t event;
    uint8_t rx_buffer[5];

    gpio_set_level(RTC_PIN,0);
    while (true)
    {
        
        if (xQueueReceive(uart_event_queue, (void*)&event,50) == pdTRUE)
        {
            switch (event.type)
            {
                case UART_DATA:

                    memset(rx_buffer,0,sizeof(rx_buffer));
                    int len = uart_read_bytes(UART_NUM_1, rx_buffer, event.size, 100);

                    if(len > 0 && rx_buffer[0] == MOTOR_ADDRESS)
                    {
                        motor_params_t param = {
                            .target_angle_deg = ((rx_buffer[1] << 8) | rx_buffer[2]) / 100.0f,
                            .direction = rx_buffer[3] & 1,
                            .half_period_us = rx_buffer[4],
                            .torque_limit = 255
                        };
                        
                        // Enforce maximum speed limit
                        if(param.half_period_us < MIN_HALF_PERIOD_US) param.half_period_us = MIN_HALF_PERIOD_US;
                        
                        ESP_LOGI(TAG, "Received command: %.2f°, %s, %dμs",
                            param.target_angle_deg,
                            param.direction ? "CW" : "CCW",
                            param.half_period_us);

                        if (xQueueSend(motor_params_queue, &param, 100) != pdTRUE) {
                            ESP_LOGE(TAG, "Failed to send motor parameters to queue");
                        }
                    }
                    memset(rx_buffer,0,sizeof(rx_buffer));
                    break;

                case UART_FRAME_ERR:

                    ESP_LOGE(TAG,"UART_FRAME_ERR");
                    break;

                default:
                    break;
            }     
        }
    }

}
void motor_control_task(void *pvParmeter)
{
    motor_params_t p;
    int pulses = 0;
    while(true)
    {
        if(xQueueReceive(motor_params_queue, &p, 50) == pdTRUE)
        {
            gpio_set_level(MOTOR_SIGN_PIN, p.direction);
            pulses = p.target_angle_deg * PULSE_PER_DEGREE;
            
            for(int i = 0; i < pulses; i++)
            {
                gpio_set_level(MOTOR_PULSE_PIN, 1);
                esp_rom_delay_us(p.half_period_us);
                gpio_set_level(MOTOR_PULSE_PIN, 0);
                esp_rom_delay_us(p.half_period_us);
            }

            // Update position tracking
            current_angle_deg += p.direction ? p.target_angle_deg : -p.target_angle_deg;

            ESP_LOGI(TAG, "Moved %.5f° %s, %d pulses", 
                p.target_angle_deg,
                p.direction ? "CW" : "CCW",
                pulses);
            
        }else 
        {
            ESP_LOGI(TAG,"Current angle: %.2f°", current_angle_deg);
        }

    }
    vTaskDelete(NULL);
}
void app_main(void)
{
    // Initialize peripherals
    uart_init();
    gpio_init();

    // Create communication queue
    motor_params_queue = xQueueCreate(MAX_QUEUE_SIZE, sizeof(motor_params_t)); 
    if (motor_params_queue == NULL) {
        ESP_LOGE(TAG, "Failed to create motor_params_queue");
        return;
    }

    // Start tasks
    xTaskCreatePinnedToCore(receive_event_task, "receive_event_task", 2048 * 2, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(motor_control_task, "motor_control_task", 2048 * 2, NULL, 5, NULL, 0);

    ESP_LOGI(TAG, "System initialized successfully");
}

void uart_init(void)
{
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT
        };
    ESP_ERROR_CHECK(uart_param_config(UART_NUM_1, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_NUM_1,UART_TXD2_PIN, UART_RXD2_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(UART_NUM_1, 1024 * 2, 1024 * 2, UART_QUEUE_SIZE, &uart_event_queue, 0));
    
}

void gpio_init(void)
{
    gpio_reset_pin(MOTOR_PULSE_PIN);
    gpio_reset_pin(MOTOR_SIGN_PIN);
    gpio_reset_pin(MOTOR_SERVO_ON);
    gpio_reset_pin(BUILT_IN_LED);

    gpio_set_direction(MOTOR_PULSE_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(MOTOR_SIGN_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(MOTOR_SERVO_ON, GPIO_MODE_OUTPUT);
    gpio_set_direction(BUILT_IN_LED, GPIO_MODE_OUTPUT);

    gpio_set_level(MOTOR_SERVO_ON, 1);

    vTaskDelay(pdMS_TO_TICKS(2000));

}

