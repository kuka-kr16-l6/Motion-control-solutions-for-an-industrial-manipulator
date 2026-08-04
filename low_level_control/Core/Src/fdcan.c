/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file    fdcan.c
 * @brief   This file provides code for the configuration
 *          of the FDCAN instances.
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
/* Includes ------------------------------------------------------------------*/
#include "fdcan.h"

/* USER CODE BEGIN 0 */

FDCAN_TxHeaderTypeDef pTxHeader;
FDCAN_FilterTypeDef sFilterConfig;

/* USER CODE END 0 */

FDCAN_HandleTypeDef hfdcan2;

/* FDCAN2 init function */
void MX_FDCAN2_Init(void)
{

  /* USER CODE BEGIN FDCAN2_Init 0 */

  /* USER CODE END FDCAN2_Init 0 */

  /* USER CODE BEGIN FDCAN2_Init 1 */

  /* USER CODE END FDCAN2_Init 1 */
  hfdcan2.Instance = FDCAN2;
  hfdcan2.Init.FrameFormat = FDCAN_FRAME_CLASSIC;
  hfdcan2.Init.Mode = FDCAN_MODE_NORMAL;
  hfdcan2.Init.AutoRetransmission = ENABLE;
  hfdcan2.Init.TransmitPause = DISABLE;
  hfdcan2.Init.ProtocolException = DISABLE;
  hfdcan2.Init.NominalPrescaler = 6;
  hfdcan2.Init.NominalSyncJumpWidth = 1;
  hfdcan2.Init.NominalTimeSeg1 = 13;
  hfdcan2.Init.NominalTimeSeg2 = 2;
  hfdcan2.Init.DataPrescaler = 1;
  hfdcan2.Init.DataSyncJumpWidth = 1;
  hfdcan2.Init.DataTimeSeg1 = 1;
  hfdcan2.Init.DataTimeSeg2 = 1;
  hfdcan2.Init.MessageRAMOffset = 0;
  hfdcan2.Init.StdFiltersNbr = 2;
  hfdcan2.Init.ExtFiltersNbr = 0;
  hfdcan2.Init.RxFifo0ElmtsNbr = 10;
  hfdcan2.Init.RxFifo0ElmtSize = FDCAN_DATA_BYTES_8;
  hfdcan2.Init.RxFifo1ElmtsNbr = 10;
  hfdcan2.Init.RxFifo1ElmtSize = FDCAN_DATA_BYTES_8;
  hfdcan2.Init.RxBuffersNbr = 0;
  hfdcan2.Init.RxBufferSize = FDCAN_DATA_BYTES_8;
  hfdcan2.Init.TxEventsNbr = 0;
  hfdcan2.Init.TxBuffersNbr = 0;
  hfdcan2.Init.TxFifoQueueElmtsNbr = 10;
  hfdcan2.Init.TxFifoQueueMode = FDCAN_TX_FIFO_OPERATION;
  hfdcan2.Init.TxElmtSize = FDCAN_DATA_BYTES_8;
  if (HAL_FDCAN_Init(&hfdcan2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN FDCAN2_Init 2 */

#if MY_NODE_TYPE == NODE_MASTER   // this for testing purpose

	pTxHeader.IdType =  FDCAN_STANDARD_ID;
	pTxHeader.TxFrameType =  FDCAN_DATA_FRAME;
	pTxHeader.DataLength = FDCAN_DLC_BYTES_8;
	pTxHeader.ErrorStateIndicator = FDCAN_ESI_ACTIVE;
	pTxHeader.BitRateSwitch = FDCAN_BRS_OFF;
	pTxHeader.FDFormat = FDCAN_CLASSIC_CAN;
	pTxHeader.TxEventFifoControl = FDCAN_NO_TX_EVENTS;
	pTxHeader.MessageMarker = 0;

#elif MY_NODE_TYPE == NODE_SLAVE

	sFilterConfig.IdType = FDCAN_STANDARD_ID;
	sFilterConfig.FilterIndex = 0;
	sFilterConfig.FilterType = FDCAN_FILTER_MASK;
	sFilterConfig.FilterConfig = FDCAN_FILTER_TO_RXFIFO0;
	sFilterConfig.FilterID1 = NODE_ID;
	sFilterConfig.FilterID2 = 0x7FF; // mask
#endif





  /* USER CODE END FDCAN2_Init 2 */

}

void HAL_FDCAN_MspInit(FDCAN_HandleTypeDef* fdcanHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(fdcanHandle->Instance==FDCAN2)
  {
  /* USER CODE BEGIN FDCAN2_MspInit 0 */

  /* USER CODE END FDCAN2_MspInit 0 */
    LL_RCC_SetFDCANClockSource(LL_RCC_FDCAN_CLKSOURCE_PLL1Q);

    /* FDCAN2 clock enable */
    __HAL_RCC_FDCAN_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**FDCAN2 GPIO Configuration
    PB5     ------> FDCAN2_RX
    PB6     ------> FDCAN2_TX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_5|GPIO_PIN_6;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    GPIO_InitStruct.Alternate = GPIO_AF9_FDCAN2;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* FDCAN2 interrupt Init */
    HAL_NVIC_SetPriority(FDCAN2_IT0_IRQn, 2, 0);
    HAL_NVIC_EnableIRQ(FDCAN2_IT0_IRQn);
  /* USER CODE BEGIN FDCAN2_MspInit 1 */

  /* USER CODE END FDCAN2_MspInit 1 */
  }
}

void HAL_FDCAN_MspDeInit(FDCAN_HandleTypeDef* fdcanHandle)
{

  if(fdcanHandle->Instance==FDCAN2)
  {
  /* USER CODE BEGIN FDCAN2_MspDeInit 0 */

  /* USER CODE END FDCAN2_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_FDCAN_CLK_DISABLE();

    /**FDCAN2 GPIO Configuration
    PB5     ------> FDCAN2_RX
    PB6     ------> FDCAN2_TX
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_5|GPIO_PIN_6);

    /* FDCAN2 interrupt Deinit */
    HAL_NVIC_DisableIRQ(FDCAN2_IT0_IRQn);
  /* USER CODE BEGIN FDCAN2_MspDeInit 1 */

  /* USER CODE END FDCAN2_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

HAL_StatusTypeDef CAN_Send_Command(uint8_t targetID, uint8_t dir, uint16_t angle, uint32_t speed)
{
	uint8_t TXheader[8];

	pTxHeader.Identifier = targetID;

	TXheader[0] = dir;
	TXheader[1] = (angle >> 8) & 0xFF;
	TXheader[2] = angle & 0xFF;
	TXheader[3] = (speed >> 24) & 0xFF;
	TXheader[4] = (speed >> 16) & 0xFF;
	TXheader[5] = (speed >> 8) & 0xFF;
	TXheader[6] = speed & 0xFF;
	TXheader[7] = 0;

	return HAL_FDCAN_AddMessageToTxFifoQ(&hfdcan2, &pTxHeader, TXheader);
}

HAL_StatusTypeDef CAN_Send_Encoder_Feedback(uint8_t targetID, uint8_t dir, float angle_deg, uint16_t speed_rpm)
{
	uint8_t TXdata[8];
	int32_t angle_x100 = (int32_t)(angle_deg * 100.0f);

	pTxHeader.Identifier = targetID;

	TXdata[0] = dir;
	TXdata[1] = (angle_x100 >> 24) & 0xFF;
	TXdata[2] = (angle_x100 >> 16) & 0xFF;
	TXdata[3] = (angle_x100 >> 8) & 0xFF;
	TXdata[4] = angle_x100 & 0xFF;
	TXdata[5] = (speed_rpm >> 8) & 0xFF;
	TXdata[6] = speed_rpm & 0xFF;
	TXdata[7] = 0xEE;

	return HAL_FDCAN_AddMessageToTxFifoQ(&hfdcan2, &pTxHeader, TXdata);
}

/* FDCAN RX FIFO 0 Callback */
void HAL_FDCAN_RxFifo0Callback(FDCAN_HandleTypeDef *hfdcan, uint32_t RxFifo0ITs)
{
	if (hfdcan->Instance == FDCAN2 && (RxFifo0ITs & FDCAN_IT_RX_FIFO0_NEW_MESSAGE) != 0)
	{
		FDCAN_RxHeaderTypeDef RxHeader;
		uint8_t RxData[8];

		while (HAL_FDCAN_GetRxFifoFillLevel(hfdcan, FDCAN_RX_FIFO0) > 0)
		{
			if (HAL_FDCAN_GetRxMessage(hfdcan, FDCAN_RX_FIFO0, &RxHeader, RxData) == HAL_OK)
			{
				uint8_t dir = RxData[0];

				float_t angle_deg = ((uint32_t)(RxData[1] << 24) |  (uint32_t)(RxData[2] << 16) |  (uint32_t)(RxData[3] << 8)|  (uint32_t)(RxData[4]))/1000.0f;

				uint16_t speed_rpm = ((uint16_t)((RxData[5] << 8) | RxData[6]));
				HAL_GPIO_TogglePin(relay_GPIO_Port, relay_Pin);

				Servo_Push_Command(dir, (angle_deg), speed_rpm);
			}
		}
	}
}

/* USER CODE END 1 */

