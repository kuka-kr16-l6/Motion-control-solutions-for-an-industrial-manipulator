# KUKA KR16 L6 Control

## Table of content
1. [Introduction](#1-Introduction)
2. [Hardware](#2-Hardware)
    - [Mechanical](#mechanical)
    - [Electrical](#electrical)
3. [Low Level Control](#3-Low-Level-Control)
4. [High Level Control](#4-High-Level-Control)
    - [Kinematics](#kinematics)
    - [Trajectory](#trajectory)
5. [About the Team](#5-About-the-Team)

## 1. Introduction

This repository contains the development work for both **low-level** and **high-level control** of the **KUKA KR16 industrial robot arm**. The project aims to bridge embedded systems with robotic motion control, offering hands-on experience in real-time control, communication protocols, and motion planning.

---

## 2. Hardware

### Mechanical

### Electrical

## 3. Low Level Control

### Overview
This module controls one joint of the KUKA KR16 L6 robot.  
It runs on an ESP32 microcontroller and communicates with a Yaskawa SERVOPACK motor driver (model SGD-180A01A).  
The code manages motor control, communication, and safety features in real-time using FreeRTOS.

### Key Features
- Real-time motor control for a single joint
- Modbus RTU communication with the high-level controller
- Safety checks: joint limits and over-travel protection
- Runs on ESP32 with FreeRTOS multitasking

### Dependencies
- ESP-IDF v5.4.1  
- FreeRTOS (built-in in ESP-IDF)  
  [FreeRTOS docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html)  
- ESP-Modbus library  
  [ESP-Modbus docs](https://docs.espressif.com/projects/esp-modbus/en/latest/esp32/)

### Hardware Interface
- ESP32 microcontroller (dual-core, 240 MHz)  
- Yaskawa SERVOPACK SGD-180A01A motor driver  
- Incremental encoder feedback  
- 25 used I/O pins for motor and communication (out of 50-pin connector)  

See the [hardware connection schematic](<INSERT-LINK-HERE>) for wiring details.

### FreeRTOS Tasks
| Core | Task Name           | Description                         | Priority  |
|-------|---------------------|-----------------------------------|-----------|
| CPU0  | motor_control_task  | Motor control and joint movement  | Normal    |
| CPU1  | receive_modbus_task | Modbus RTU communication          | Normal    |

### Inputs and Outputs
- **Inputs:** Desired joint position, direction, speed, torque limits, Modbus messages  
- **Outputs:** Motor control signals to SERVOPACK, status feedback to high-level controller

### Integration
- Controlled by the high-level controller via Modbus RTU  
- See [high-level main code controller ](<INSERT_HIGH_LEVEL_REPO_LINK>) for more details

### Running & Testing
- Deployed directly on the ESP32 hardware on the robot joint  
- Not currently supported for simulation

You can view the implementation in this file:  
👉 [main source code](./low_level_control/slave.c)


## 4. High Level Control

### Kinematics

### Trajectory


## 5. About the Team

We are a team of **Mechatronics and Robotics Engineering students** working on this project under the guidance of our academic supervisors.

### 🧑‍🏫 Supervisors

We are grateful for the support and mentorship of our supervisors:
- Dr. Ahmed Saad
- Dr. Gamal Abd Elnaser

- 🔧 **Focus**: Low-level motor and sensor interfacing, real-time control, and high-level task planning  
- 🧪 **Technologies**: Embedded C/C++, FreeRTOS, industrial communication protocols RS485 & Modbus RTU
- 🎓 **Goal**: Gain industry-ready experience and contribute to open robotic systems

---

## 📄 License

This project is licensed under the [Apache 2.0 License](./LICENSE) – feel free to use, modify, and contribute with attribution.

---

