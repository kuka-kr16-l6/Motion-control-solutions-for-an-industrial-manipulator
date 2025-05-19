#include <stdio.h>
#include <stdint.h>
#include "esp_err.h"
#include "mbcontroller.h"       
#include "modbus_params.h"      
#include "esp_log.h"            
#include "sdkconfig.h"
#include "driver/gpio.h"

#define MB_PORT_NUM     UART_NUM_0   
#define MB_SLAVE_ADDR    7           
#define MB_DEV_SPEED    115200       
#define LED_GPIO 2

static const char *TAG = "SLAVE_TEST";

static portMUX_TYPE param_lock = portMUX_INITIALIZER_UNLOCKED;

// Set register values into known state
static void setup_reg_data(void)
{
    holding_reg_params.direction = 0; // 0 = CW, 1 = CCW
    holding_reg_params.angle = 0.0;   // Initial angle
}

static void setup_led(void)
{
    gpio_reset_pin(LED_GPIO);
    gpio_set_level(LED_GPIO, 0); // LED OFF initially
}
void app_main(void) {
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

    ESP_LOGI(TAG, "Modbus slave stack initialized.");
    ESP_LOGI(TAG, "Start modbus test...");
    uint8_t last_led_state = 0xFF;
    while (1) {
        // Check for read/write events of Modbus master for certain events
        (void)mbc_slave_check_event(MB_EVENT_HOLDING_REG_RD | MB_EVENT_HOLDING_REG_WR);
        ESP_ERROR_CHECK_WITHOUT_ABORT(mbc_slave_get_param_info(&reg_info, 10));

        if (reg_info.type & (MB_EVENT_HOLDING_REG_WR | MB_EVENT_HOLDING_REG_RD)) {
            const char* rw_str = (reg_info.type & MB_EVENT_HOLDING_REG_RD) ? "READ" : "WRITE";
            ESP_LOGI(TAG, "HOLDING %s (%" PRIu32 " us), ADDR:%u, TYPE:%u, INST_ADDR:0x%" PRIx32 ", SIZE:%u",
                        rw_str,
                        reg_info.time_stamp,
                        (unsigned)reg_info.mb_offset,
                        (unsigned)reg_info.type,
                        (uint32_t)reg_info.address,
                        (unsigned)reg_info.size);

            // Example: Act on new values
            // portENTER_CRITICAL(&param_lock);
            // uint8_t curr_direction = holding_reg_params.direction;
            // float curr_angle = holding_reg_params.angle;
            // portEXIT_CRITICAL(&param_lock);

            // ESP_LOGI(TAG, "Direction: %u, Angle: %.2f", curr_direction, curr_angle);
            
           portENTER_CRITICAL(&param_lock);
           uint8_t curr_led_state  = holding_reg_params.direction;
           portEXIT_CRITICAL(&param_lock);
           if (curr_led_state != last_led_state) gpio_set_level(LED_GPIO, (curr_led_state ? 1 : 0));
           last_led_state  = curr_led_state;
           ESP_LOGI(TAG, "LED State changed to: %s", curr_led_state ? "ON" : "OFF");
        }
        vTaskDelay(100 / portTICK_PERIOD_MS); // Polling interval
    }
    // Destroy Modbus controller (not reached in this loop)
    ESP_LOGI(TAG,"Modbus controller destroyed.");
    vTaskDelay(100 / portTICK_PERIOD_MS);
    ESP_ERROR_CHECK(mbc_slave_destroy());
}
