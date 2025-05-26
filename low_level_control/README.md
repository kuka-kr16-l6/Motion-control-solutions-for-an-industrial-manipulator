# Low Level Control Module for KUKA KR16 L6 Robot

## Overview
This module controls one joint of the KUKA KR16 L6 robot.  
It runs on an ESP32 microcontroller and communicates with a Yaskawa SERVOPACK motor driver (model SGD-180A01A).  
The code manages motor control, communication, and safety features in real-time using FreeRTOS.

## Key Features
- Real-time motor control for a single joint
- Modbus RTU communication with the high-level controller
- Safety checks: joint limits and over-travel protection
- Runs on ESP32 with FreeRTOS multitasking

## Project Structure
mb_slave
├── main
│ └── slave.c # Main control logic for this joint


## Dependencies
- ESP-IDF v5.4.1  
- FreeRTOS (built-in in ESP-IDF)  
  [FreeRTOS docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html)  
- ESP-Modbus library  
  [ESP-Modbus docs](https://docs.espressif.com/projects/esp-modbus/en/latest/esp32/)

## Hardware Interface
- ESP32 microcontroller (dual-core, 240 MHz)  
- Yaskawa SERVOPACK SGD-180A01A motor driver  
- Incremental encoder feedback  
- 25 used I/O pins for motor and communication (out of 50-pin connector)  

See the [hardware connection schematic](<INSERT-LINK-HERE>) for wiring details.

## FreeRTOS Tasks
| Core | Task Name           | Description                         | Priority  |
|-------|---------------------|-----------------------------------|-----------|
| CPU0  | motor_control_task  | Motor control and joint movement  | Normal    |
| CPU1  | receive_modbus_task | Modbus RTU communication          | Normal    |

## Inputs and Outputs
- **Inputs:** Desired joint position, direction, speed, torque limits, Modbus messages  
- **Outputs:** Motor control signals to SERVOPACK, status feedback to high-level controller

## Integration
- Controlled by the high-level controller via Modbus RTU  
- Future plans to integrate with ROS 2 middleware  
- See [high-level controller ](<INSERT_HIGH_LEVEL_REPO_LINK>) for more

## Running & Testing
- Deployed directly on the ESP32 hardware on the robot joint  
- Not currently supported for simulation

