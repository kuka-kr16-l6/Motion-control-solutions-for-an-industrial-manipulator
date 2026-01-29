/*
 * servo.h
 *
 *  Created on: Jan 28, 2026
 *      Author: ahmed
 */

#ifndef SERVO_H
#define SERVO_H

#include "stm32f4xx_hal.h"
#include <stdint.h>

typedef enum {
    SERVO_IDLE = 0,
    SERVO_BUSY,
	SERVO_DONE
} Servo_State_t;

typedef struct {
    TIM_HandleTypeDef *htim_pwm;   // Pointer to TIM1
    TIM_HandleTypeDef *htim_count; // Pointer to TIM2
    GPIO_TypeDef *port;            // Port for DIR pin (e.g., GPIOA)
    uint16_t pin;                  // Pin for DIR pin (e.g., GPIO_PIN_5)
    volatile Servo_State_t state;
} Servo_HandleTypeDef;

//typedef struct {
//    uint32_t pulses;            // RTOS LATER
//    uint32_t freq_hz;
//    uint8_t  dir;
//} Servo_Command_t;

void Servo_Init(Servo_HandleTypeDef *servo, TIM_HandleTypeDef *htim_pwm, TIM_HandleTypeDef *htim_count);

void Servo_Move(Servo_HandleTypeDef *servo, uint32_t pulses, uint32_t freq_hz, uint8_t dir);

void Servo_TIM2_IRQHandler(Servo_HandleTypeDef *servo);

#endif // SERVO_H
