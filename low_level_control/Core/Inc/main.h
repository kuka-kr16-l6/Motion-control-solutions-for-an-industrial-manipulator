/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32h7xx_hal.h"

#include "stm32h7xx_ll_rcc.h"
#include "stm32h7xx_ll_crs.h"
#include "stm32h7xx_ll_bus.h"
#include "stm32h7xx_ll_system.h"
#include "stm32h7xx_ll_exti.h"
#include "stm32h7xx_ll_cortex.h"
#include "stm32h7xx_ll_utils.h"
#include "stm32h7xx_ll_pwr.h"
#include "stm32h7xx_ll_dma.h"
#include "stm32h7xx_ll_tim.h"
#include "stm32h7xx_ll_gpio.h"
#include "stm32h7xx_ll_hsem.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define brake_Pin LL_GPIO_PIN_2
#define brake_GPIO_Port GPIOE
#define relay_Pin LL_GPIO_PIN_3
#define relay_GPIO_Port GPIOE
#define clear_Pin LL_GPIO_PIN_0
#define clear_GPIO_Port GPIOA
#define dir_Pin LL_GPIO_PIN_1
#define dir_GPIO_Port GPIOA
#define ServoReady_Pin LL_GPIO_PIN_12
#define ServoReady_GPIO_Port GPIOB
#define ServoReady_EXTI_IRQn EXTI15_10_IRQn
#define servo_on_Pin LL_GPIO_PIN_15
#define servo_on_GPIO_Port GPIOD
#define led1_Pin LL_GPIO_PIN_10
#define led1_GPIO_Port GPIOA

/* USER CODE BEGIN Private defines */

#define JOINT_1			1
#define JOINT_2			2
#define JOINT_3			3
#define JOINT_4			4
#define JOINT_5			5
#define JOINT_6			6


#define NODE_SLAVE_ID	JOINT_5



/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
