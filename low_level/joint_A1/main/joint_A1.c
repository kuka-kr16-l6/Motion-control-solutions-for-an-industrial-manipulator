#include <stdio.h>
#include "driver/uart.h"
#include <driver/gpio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/idf_additions.h>
#include <string.h>
#include <esp_log.h>

#define BUILT_IN_LED 2
#define TXD2 17
#define RXD2 16
#define TXD0 1
#define RXD0 3
#define RTC 12

#define PULSE 13
#define SIGN 14
#define SON 27
#define PULSE_PER_DEGREE  700
#define MAX_freq 8

typedef struct {
    float target_degree;    // Target position
    bool direction;         // Direction of rotation
    uint8_t torque_limit;       // Torque limit (if applicable)
    uint8_t frequancy;          // target frequancy
} motor_params_t;

static const char* TAG = "Joint_A1";

QueueHandle_t uart_event_queue;
QueueHandle_t motor_params_queue = NULL;


uint8_t rx_buffer[5];
int pulses = 0;
int counter = 0;
float deg = 0;


void uart_init(void);
void gpio_init(void);
void RS485_Send(uart_port_t uart_port,uint8_t* buf,uint16_t size);


void receive_event_task(void *pvParameter)
{

    uart_event_t event;
    gpio_set_level(RTC,0);
    while (1)
    {
        
        if (xQueueReceive(uart_event_queue, (void*)&event,50) == pdTRUE)
        {
            switch (event.type)
            {
                
                case UART_DATA:
                    memset(rx_buffer,0,sizeof(rx_buffer));
                    int len = uart_read_bytes(UART_NUM_1, rx_buffer, event.size, 100);
                    if(len > 0 && rx_buffer[0] == 1)
                    {
                        motor_params_t param = {0};
                        
                        param.target_degree = ((rx_buffer[1] << 8) + rx_buffer[2]) / 100.0;
                        param.direction = rx_buffer[3]&1;
                        param.frequancy = rx_buffer[4];
                        param.torque_limit = 255;

                        if(param.frequancy < MAX_freq)param.frequancy = MAX_freq;
                        
                        ESP_LOGI(TAG, "Received data: %0.3f degree, %d direction, %d torque_limit, %d speed", 
                            param.target_degree, param.direction, param.torque_limit, param.frequancy);
                        if (xQueueSend(motor_params_queue, &param, 100) != pdTRUE) {
                            ESP_LOGE(TAG, "Failed to send motor parameters to queue");
                        }
                        // gpio_set_level(BUILT_IN_LED,1);
                        // vTaskDelay(pdMS_TO_TICKS(300));
                        // gpio_set_level(BUILT_IN_LED,0);
                    }
                    memset(rx_buffer,0,sizeof(rx_buffer));
                    break;

                case UART_FRAME_ERR:

                    ESP_LOGE(TAG,"UART_FRAME_ERR");
                    break;
                    default:break;
            }     
        }
    }

}
void motor_control_task(void *pvParmeter)
{
    motor_params_t p;
    while(1)
    {
        if(xQueueReceive(motor_params_queue, &p, 50) == pdTRUE)
        {
            counter++;
            gpio_set_level(SIGN, p.direction);
            pulses = p.target_degree * PULSE_PER_DEGREE;
            
            for(int i=0;i<pulses;i++)
            {
                gpio_set_level(PULSE, 1);
                esp_rom_delay_us(p.frequancy);
                gpio_set_level(PULSE, 0);
                esp_rom_delay_us(p.frequancy);
            }
            if(p.direction == 1)deg += p.target_degree;
            else deg-= p.target_degree;
            ESP_LOGI(TAG, "motor moved : %0.6f degree in %d direction with %d speed.",p.target_degree,p.direction,p.frequancy);
        }else 
        {
            ESP_LOGI(TAG,"%0.2f degree, %d number of message.",deg, counter);
        }
    }
    vTaskDelete(NULL);
}
void app_main(void)
{
    uart_init();
    gpio_init();

    motor_params_queue = xQueueCreate(100, sizeof(motor_params_t)); 
    if (motor_params_queue == NULL) {
        ESP_LOGE(TAG, "Failed to create motor_params_queue");
        return;
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);

    xTaskCreatePinnedToCore(receive_event_task, "receive_event_task", 2048 * 2, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(motor_control_task, "motor_control_task", 2048 * 2, NULL, 5, NULL, 0);

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
    ESP_ERROR_CHECK(uart_set_pin(UART_NUM_1,TXD2, RXD2,UART_PIN_NO_CHANGE,UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(UART_NUM_1, 1024 * 2, 1024 * 2, 30, &uart_event_queue, 0));
    
}
void RS485_Send(uart_port_t uart_port,uint8_t* buf,uint16_t size)
{
    gpio_set_level(RTC,1);
    uart_write_bytes(uart_port,buf,size);
    ESP_ERROR_CHECK(uart_wait_tx_done(uart_port, 100));
    gpio_set_level(RTC,0);
}
void gpio_init(void)
{
    gpio_reset_pin(PULSE);
    gpio_reset_pin(SIGN);
    gpio_reset_pin(SON);
    gpio_reset_pin(BUILT_IN_LED);

    gpio_set_direction(PULSE, GPIO_MODE_OUTPUT);
    gpio_set_direction(SIGN, GPIO_MODE_OUTPUT);
    gpio_set_direction(SON, GPIO_MODE_OUTPUT);
    gpio_set_direction(BUILT_IN_LED, GPIO_MODE_OUTPUT);

    gpio_set_level(SON, 1);
    vTaskDelay(pdMS_TO_TICKS(3000));

}

