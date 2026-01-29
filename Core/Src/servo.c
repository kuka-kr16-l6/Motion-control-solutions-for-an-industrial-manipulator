/*
 * servo.c
 *
 *  Created on: Jan 28, 2026
 *      Author: ahmed
 */
#include "servo.h"
#include "main.h"

void Servo_Init(Servo_HandleTypeDef *servo, TIM_HandleTypeDef *htim_pwm, TIM_HandleTypeDef *htim_count)
{
	servo->state = SERVO_IDLE;
	servo->htim_pwm   = htim_pwm;
	servo->htim_count = htim_count;

/* TIM1 preload enable */
	servo->htim_pwm->Instance->CR1   |= TIM_CR1_ARPE;
	servo->htim_pwm->Instance->CCMR1 |= TIM_CCMR1_OC1PE;

/* TIM2 external clock mode (clean config) */
	servo->htim_count->Instance->SMCR = (TIM_SMCR_SMS_2 | TIM_SMCR_SMS_1 | TIM_SMCR_SMS_0) | TIM_SMCR_TS_0;

	servo->htim_count->Instance->DIER |= TIM_DIER_UIE;
	servo->htim_count->Instance->CNT = 0;
}


static void Servo_SetFrequency(TIM_HandleTypeDef *htim, uint32_t freq_hz)
{
    const uint32_t timer_clk = 84000000UL;

    // Clamp frequency to your specific range
    if (freq_hz < 10)    freq_hz = 10;
    if (freq_hz > 50000) freq_hz = 50000;

    uint32_t prescaler = (timer_clk / (freq_hz * 65536));

    // 2. Calculate ARR
    uint32_t arr = (timer_clk / ((prescaler + 1) * freq_hz)) - 1;

    // 3. Safety check for ARR (should not happen with the logic above)
    if (arr > 0xFFFF) arr = 0xFFFF;

    // 4. Update Hardware Registers
    htim->Instance->PSC  = (uint16_t)prescaler;
    htim->Instance->ARR  = (uint16_t)arr;
    htim->Instance->CCR1 = (uint16_t)((arr + 1) / 2); // Square wave

    // Force immediate update of shadow registers
    htim->Instance->EGR = TIM_EGR_UG;
}

void Servo_Move(Servo_HandleTypeDef *servo, uint32_t pulses, uint32_t freq_hz, uint8_t dir)
{
	if (servo->state != SERVO_IDLE)
	        return;

	    servo->state = SERVO_BUSY;

    if (pulses == 0) return;

    /* Stop timers */
    servo->htim_pwm->Instance->CR1 &= ~TIM_CR1_CEN;
    servo->htim_count->Instance->CR1 &= ~TIM_CR1_CEN;
    servo->htim_pwm->Instance->BDTR &= ~TIM_BDTR_MOE;

    /* Direction */
    HAL_GPIO_WritePin(servo->port, servo->pin,
                      dir ? GPIO_PIN_SET : GPIO_PIN_RESET);

    /* Frequency */
    Servo_SetFrequency(servo->htim_pwm, freq_hz);

    /* Pulse count */
    servo->htim_count->Instance->ARR = pulses - 1;
    servo->htim_count->Instance->CNT = 0;

    /* Update + clear flags */
    servo->htim_pwm->Instance->EGR  = TIM_EGR_UG;
    servo->htim_count->Instance->EGR = TIM_EGR_UG;
    servo->htim_count->Instance->SR = 0;

    /* Start slave first */
    servo->htim_count->Instance->CR1 |= TIM_CR1_CEN;

    /* Start master */
    servo->htim_pwm->Instance->CCER |= TIM_CCER_CC1E;
    servo->htim_pwm->Instance->BDTR |= TIM_BDTR_MOE;
    servo->htim_pwm->Instance->CR1  |= TIM_CR1_CEN;
}

void Servo_TIM2_IRQHandler(Servo_HandleTypeDef *servo)
{

//	BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    if (servo->htim_count->Instance->SR & TIM_SR_UIF)
    {
        /* Stop everything */
        servo->htim_pwm->Instance->CR1 &= ~TIM_CR1_CEN;
        servo->htim_pwm->Instance->BDTR &= ~TIM_BDTR_MOE;
        servo->htim_pwm->Instance->CCER &= ~TIM_CCER_CC1E;
        servo->htim_count->Instance->CR1 &= ~TIM_CR1_CEN;

        servo->state = SERVO_DONE;

        /* Clear all flags */
        servo->htim_count->Instance->SR = 0;

//        vTaskNotifyGiveFromISR(servoTaskHandle, &xHigherPriorityTaskWoken);

        HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
    }
}

//void ServoTask(void *argument)
//{
//    Servo_Command_t cmd;
//
//    for (;;)
//    {
//        /* 1. Wait for a motion command */
//        if (xQueueReceive(servoQueue, &cmd, portMAX_DELAY) == pdPASS)
//        {
//            /* 2. Start motion */
//            Servo_Move(&servo, cmd.pulses, cmd.freq_hz, cmd.dir);
//
//            /* 3. Wait for completion (from ISR) */
//            ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
//
//            /* 4. Motion finished */
//            servo.state = SERVO_IDLE;
//        }
//    }
//}
