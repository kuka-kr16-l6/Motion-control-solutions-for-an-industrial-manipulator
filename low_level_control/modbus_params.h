/*
 * SPDX-FileCopyrightText: 2016-2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/*=====================================================================================
 * Description:
 *   The Modbus parameter structures used to define Modbus instances that
 *   can be addressed by Modbus protocol. Define these structures per your needs in
 *   your application. Below is just an example of possible parameters.
 *====================================================================================*/
#ifndef _DEVICE_PARAMS
#define _DEVICE_PARAMS

#include <stdint.h>
#pragma pack(push, 1)
typedef struct
{
    uint8_t direction;  // 0->cw, 1->ccw
    float angle;        // 0 ~ 180
    float half_period;
    float torque_limit;
} holding_reg_params_t;
#pragma pack(pop)

extern holding_reg_params_t holding_reg_params;

#endif // !defined(_DEVICE_PARAMS)
