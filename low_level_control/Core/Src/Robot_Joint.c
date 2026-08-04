/*
 * Robot_Joint.c
 */
#include "Robot_Joint.h"
#include "main.h"


extern TIM_HandleTypeDef htim1;

static volatile Servo_FIFO_t servo_drive = {0};

static float pulse_error_accumulator = 0.0f;

static void Servo_PTO(void);

static volatile uint32_t servo_overflow_count = 0;   // add this

uint32_t Servo_Get_Overflow_Count(void)
{
	return servo_overflow_count;
}

void Servo_Init(void)
{
	__disable_irq();
	servo_drive.head = 0;
	servo_drive.tail = 0;
	servo_drive.count = 0;
	servo_drive.is_busy = false;
	__enable_irq();

	// Reset Driver
	HAL_GPIO_WritePin(clear_GPIO_Port, clear_Pin, GPIO_PIN_SET);
	HAL_Delay(100);
	HAL_GPIO_WritePin(clear_GPIO_Port, clear_Pin, GPIO_PIN_RESET);
}

void Servo_Enable(bool enable)
{
	HAL_GPIO_WritePin(servo_on_GPIO_Port, servo_on_Pin, enable ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

void Motor_Brake(bool enable)
{
	HAL_GPIO_WritePin(brake_GPIO_Port, brake_Pin, enable ? GPIO_PIN_RESET : GPIO_PIN_SET);
}

bool Servo_Is_Busy(void)
{
	return servo_drive.is_busy;
}

static void Servo_PTO(void)
{
	ServoCmd_t cmd;
	bool has_cmd = false;

	__disable_irq();
	if (servo_drive.count > 0)
	{
		cmd = servo_drive.queue[servo_drive.tail];
		servo_drive.tail = (servo_drive.tail + 1) % FIFO_SIZE;
		servo_drive.count--;
		servo_drive.is_busy = true;
		has_cmd = true;
	}
	else
	{
		servo_drive.is_busy = false;
	}
	__enable_irq();

	if (!has_cmd) return;

	// 1. Set Direction
	if (NODE_SLAVE_ID == JOINT_3 || NODE_SLAVE_ID == JOINT_5)
		HAL_GPIO_WritePin(dir_GPIO_Port, dir_Pin, cmd.dir? GPIO_PIN_RESET : GPIO_PIN_SET);
	else
		HAL_GPIO_WritePin(dir_GPIO_Port, dir_Pin, cmd.dir ? GPIO_PIN_SET : GPIO_PIN_RESET);


	// 2. Prepare Timer Registers
	TIM1->CR1 &= ~TIM_CR1_CEN;
	TIM1->CR1 |= TIM_CR1_UDIS;

	TIM1->ARR  = cmd.arr_value;
	TIM1->CCR1 = (cmd.arr_value + 1) / 2;
	TIM1->RCR  = cmd.pulses - 1;

	TIM1->CNT = 0;
	TIM1->CR1 &= ~TIM_CR1_UDIS;
	TIM1->EGR = TIM_EGR_UG;
	TIM1->SR &= ~TIM_SR_UIF;

	// 3. Enable One Pulse Mode and Update Interrupt
	TIM1->CR1 |= TIM_CR1_OPM;
	__HAL_TIM_ENABLE_IT(&htim1, TIM_IT_UPDATE);

	// 4. Start Hardware Output
	TIM1->CCER |= TIM_CCER_CC1E;   // Enable Channel 1 Output
	TIM1->BDTR |= TIM_BDTR_MOE;    // Main Output Enable (Crucial for TIM1)
	TIM1->CR1  |= TIM_CR1_CEN;     // Go!
}

void Servo_Fault_Handler(bool driver_ready)
{
    if (driver_ready)
    {
        Motor_Brake(false);
        Servo_Enable(true);
    }
    else
    {
        Servo_Enable(false);
        Motor_Brake(true);

        TIM1->CR1 &= ~TIM_CR1_CEN;
        __HAL_TIM_DISABLE_IT(&htim1, TIM_IT_UPDATE);

        __disable_irq();
        servo_drive.head = 0;
        servo_drive.tail = 0;
        servo_drive.count = 0;
        servo_drive.is_busy = false;
        __enable_irq();

        pulse_error_accumulator = 0.0f;
        // set fault/needs_rehome flag for motion planner here
    }
}

bool Servo_Push_Command(uint8_t dir, float_t angle, uint16_t speed_RPM)
{
	if (speed_RPM == 0) return false;


	uint32_t Speed_Hz = speed_RPM * SpeedHz;

	uint32_t arr = (1000000 / Speed_Hz) - 1;
	if (arr > 65535) arr = 65535;

	float exact_pulses = angle * PULSE_PER_DEGREE;

	float total_pulses_needed = exact_pulses + pulse_error_accumulator;

	uint32_t pulses = (uint32_t)total_pulses_needed;

	float leftover_error = total_pulses_needed - (float)pulses;

	if (pulses == 0)
	{
		pulse_error_accumulator = leftover_error;
		return true;
	}

	ServoCmd_t cmd = { .dir = dir, .pulses = pulses, .arr_value = arr };

	__disable_irq();
	if (servo_drive.count >= FIFO_SIZE)
	{
		servo_overflow_count++;
		__enable_irq();
		return false;
	}

	pulse_error_accumulator = leftover_error;

	servo_drive.queue[servo_drive.head] = cmd;
	servo_drive.head = (servo_drive.head + 1) % FIFO_SIZE;
	servo_drive.count++;

	bool start = !servo_drive.is_busy;
	__enable_irq();

	if (start) Servo_PTO();

	return true;
}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	if (htim->Instance == TIM1)
	{
		__HAL_TIM_DISABLE_IT(&htim1, TIM_IT_UPDATE);
		Servo_PTO();
	}
}
