#include <stdio.h>
#include <stdint.h>
#include "driver/uart.h"
#include <driver/gpio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/idf_additions.h>
#include <string.h>
#include <esp_log.h>
#include "esp_err.h"
#include "mbcontroller.h"       
#include "modbus_params.h"
#include "sdkconfig.h"

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

// ModBus
#define MB_PORT_NUM     UART_NUM_0   
#define MB_SLAVE_ADDR    7           
#define MB_DEV_SPEED    115200       
#define LED_GPIO 2

typedef struct {
    float target_angle_deg;    
    bool direction;         
    uint8_t torque_limit;       
    uint8_t half_period_us;     
} motor_params_t;

static portMUX_TYPE param_lock = portMUX_INITIALIZER_UNLOCKED;
QueueHandle_t uart_event_queue;
QueueHandle_t motor_params_queue = NULL;

static float current_angle_deg = 0.00f;

void uart_init(void);
void gpio_init(void);
static void setup_reg_data(void);
void modbus_init(void);

// Task handling incoming UART data
void recieve_modbus_task(void *pvParameter){
    
    ESP_LOGI(TAG, "Modbus slave stack initialized.");
    ESP_LOGI(TAG, "Start modbus test...");
    while (1) {
        // Check for read/write events of Modbus master for certain events
        (void)mbc_slave_check_event(MB_EVENT_HOLDING_REG_RD | MB_EVENT_HOLDING_REG_WR);
        ESP_ERROR_CHECK_WITHOUT_ABORT(mbc_slave_get_param_info(&reg_info, 10));

        if (reg_info.type & (MB_EVENT_HOLDING_REG_WR | MB_EVENT_HOLDING_REG_RD)) {
            // const char* rw_str = (reg_info.type & MB_EVENT_HOLDING_REG_RD) ? "READ" : "WRITE";
            // ESP_LOGI(TAG, "HOLDING %s (%" PRIu32 " us), ADDR:%u, TYPE:%u, INST_ADDR:0x%" PRIx32 ", SIZE:%u",
            //             rw_str,
            //             reg_info.time_stamp,
            //             (unsigned)reg_info.mb_offset,
            //             (unsigned)reg_info.type,
            //             (uint32_t)reg_info.address,
            //             (unsigned)reg_info.size);

            // Example: Act on new values
            // portENTER_CRITICAL(&param_lock);
            // uint8_t curr_direction = holding_reg_params.direction;
            // float curr_angle = holding_reg_params.angle;
            // portEXIT_CRITICAL(&param_lock);

            // ESP_LOGI(TAG, "Direction: %u, Angle: %.2f", curr_direction, curr_angle);
            
           portENTER_CRITICAL(&param_lock);
           motor_params_t param = {
                            .target_angle_deg =  holding_reg_params.angle,
                            .direction =  holding_reg_params.direction,
                            .half_period_us =  holding_reg_params.half_period,
                            .torque_limit = 255
                        };
            if (xQueueSend(motor_params_queue, &param, 100) != pdTRUE) {
                ESP_LOGE(TAG, "Failed to send motor parameters to queue");
            }
            
           portEXIT_CRITICAL(&param_lock);
           ESP_LOGI(TAG, "received %.3f degree, %d direction, %d delay.", param.target_angle_deg, param.direction, param.half_period_us);
        }
        vTaskDelay(100 / portTICK_PERIOD_MS); // Polling interval
    }
    vTaskDelete(NULL);
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
    
    gpio_init();
    modbus_init();
    
    // Create communication queue
    motor_params_queue = xQueueCreate(MAX_QUEUE_SIZE, sizeof(motor_params_t)); 
    if (motor_params_queue == NULL) {
        ESP_LOGE(TAG, "Failed to create motor_params_queue");
        return;
    }

    // Start tasks
    xTaskCreatePinnedToCore(recieve_modbus_task, "receive_event_task", 2048 * 2, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(motor_control_task, "motor_control_task", 2048 * 2, NULL, 5, NULL, 0);

    ESP_LOGI(TAG, "System initialized successfully");
}
void modbus_init(void){
    mb_param_info_t reg_info; 
    mb_communication_info_t comm_info; 
    mb_register_area_descriptor_t reg_area; 

    
    esp_log_level_set(TAG, ESP_LOG_INFO);
    void* mbc_slave_handler = NULL;

    ESP_ERROR_CHECK(mbc_slave_init(MB_PORT_SERIAL_SLAVE, &mbc_slave_handler)); 

    // Setup communication mode and start stack
#if CONFIG_MB_COMM_MODE_ASCII
    comm_info.mode = MB_MODE_ASCII;
#elif CONFIG_MB_COMM_MODE_RTU
    comm_info.mode = MB_MODE_RTU;
#endif
    comm_info.slave_addr = MB_SLAVE_ADDR;
    comm_info.port = MB_PORT_NUM;
    comm_info.baudrate = MB_DEV_SPEED;
    comm_info.parity = MB_PARITY_NONE;
    ESP_ERROR_CHECK(mbc_slave_setup((void*)&comm_info));

    // Register the holding register area for direction and angle
    reg_area.type = MB_PARAM_HOLDING;
    reg_area.start_offset = 0; // Start at Modbus holding register 0
    reg_area.address = (void*)&holding_reg_params;
    reg_area.size = sizeof(holding_reg_params); // Should be 5 bytes (covers direction + angle)
    ESP_ERROR_CHECK(mbc_slave_set_descriptor(reg_area));

    setup_reg_data(); // Set values into known state
    setup_led();

    // Starts modbus controller and stack
    ESP_ERROR_CHECK(mbc_slave_start());

    // Set UART pin numbers
    ESP_ERROR_CHECK(uart_set_pin(MB_PORT_NUM, CONFIG_MB_UART_TXD,
                            CONFIG_MB_UART_RXD, CONFIG_MB_UART_RTS,
                            UART_PIN_NO_CHANGE));

    // Set UART driver mode to Half Duplex
    ESP_ERROR_CHECK(uart_set_mode(MB_PORT_NUM, UART_MODE_RS485_HALF_DUPLEX));
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

static void setup_reg_data(void)
{
    holding_reg_params.direction = 0; // 0 = CW, 1 = CCW
    holding_reg_params.angle = 0.0;   // Initial angle
}

