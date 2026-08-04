/*
 * Robot_Joint.h
 *
 *  Created on: Feb 18, 2026
 *      Author: ahmed magdy
 */

#ifndef INC_ROBOT_JOINT_H_
#define INC_ROBOT_JOINT_H_

#include "stm32h7xx_hal.h"
#include "main.h"
#include <stdbool.h>

#define FIFO_SIZE            10000
#define TIM1_CLK             168000000
#define PULSE_PER_DEGREE_1   2000
#define PULSE_PER_DEGREE_2   2000
#define PULSE_PER_DEGREE_3   2000
#define PULSE_PER_DEGREE_4   2010
#define PULSE_PER_DEGREE_5   1900
#define PULSE_PER_DEGREE_6   1900

#define Gear_Joint_1       	 125
#define Gear_Joint_2       	 125
#define Gear_Joint_3         125
#define Gear_Joint_4         74.444           //670 : 9
#define Gear_Joint_5         42.222           // 380 : 9
#define Gear_Joint_6         24.117           // 410 : 17

#define SpeedHz_j1           (6/Gear_Joint_1*PULSE_PER_DEGREE_1)
#define SpeedHz_j2           (6/Gear_Joint_2*PULSE_PER_DEGREE_2)
#define SpeedHz_j3           (6/Gear_Joint_3*PULSE_PER_DEGREE_3)
#define SpeedHz_j4           (6/Gear_Joint_4*PULSE_PER_DEGREE_4)
#define SpeedHz_j5           (6/Gear_Joint_5*PULSE_PER_DEGREE_5)
#define SpeedHz_j6           (6/Gear_Joint_6*PULSE_PER_DEGREE_6)

#if NODE_SLAVE_ID == JOINT_1
    #define SpeedHz 		    SpeedHz_j1
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_1
#elif NODE_SLAVE_ID == JOINT_2
    #define SpeedHz 			SpeedHz_j2
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_2
#elif NODE_SLAVE_ID == JOINT_3
    #define SpeedHz 			SpeedHz_j3
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_3
#elif NODE_SLAVE_ID == JOINT_4
    #define SpeedHz 			SpeedHz_j4
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_4
#elif NODE_SLAVE_ID == JOINT_5
    #define SpeedHz 			SpeedHz_j5
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_5
#elif NODE_SLAVE_ID == JOINT_6
    #define SpeedHz 			SpeedHz_j6
	#define PULSE_PER_DEGREE   	PULSE_PER_DEGREE_6
#else

    #error "Invalid NODE_SLAVE_ID"

#endif
typedef struct {
	uint8_t  dir;
	uint32_t pulses;
	uint32_t arr_value;
} ServoCmd_t;

typedef struct {
	ServoCmd_t queue[FIFO_SIZE];
	volatile uint16_t head;
	volatile uint16_t tail;
	volatile uint16_t count;
	volatile bool is_busy;
} Servo_FIFO_t;

void Servo_Init(void);
void Servo_Fault_Handler(bool driver_ready);
uint32_t Servo_Get_Overflow_Count(void);
bool Servo_Push_Command(uint8_t dir, float_t angle, uint16_t speed_RPM);
bool Servo_Is_Busy(void);
void Servo_Enable(bool enable);
void Motor_Brake(bool enable);

#endif /* INC_ROBOT_JOINT_H_ */
