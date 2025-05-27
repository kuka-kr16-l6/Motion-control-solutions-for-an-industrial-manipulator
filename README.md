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

## Kinematics
- [Forward Kinematics](#denavit-hartenberg-diagram)
- [Inverse Kinematics](#inverse-kinematics-ik)
- [Jacobian Matrix](#jacobian-matrix)

### Robot Kinematics Model – KUKA KR16 L6

This module defines the kinematic structure of the **KUKA KR16 L6** robotic arm using the **Denavit-Hartenberg (DH)** convention.
It includes geometric parameters and a method to compute the homogeneous transformation matrix for each link.

---


###  Features

- Defines full Denavit-Hartenberg parameters for the KUKA KR16 L6 robot

- Provides a method to compute the homogeneous transformation matrix for any link

- Includes joint limits for all 6 revolute joints

- Designed for easy integration with inverse kinematics, Jacobian computation, and simulation modules

- Lightweight and efficient using NumPy arrays for matrix operations

---

###  Configuration Guide

For a complete breakdown of the kinematic model configuration, joint parameters, and transformation setup, refer to the documentation:

- [🔧 Robot Configuration Documentation (PDF)](./hardware/mechanical/data/db_kr_16_l6_en.pdf)


This document supports the implementation and can help you verify or customize the DH model used in the code.


You can view the implementation in this file:  
👉 [Parameters Implementation](./high_level_control/parameters/robot.py)

[//]: # (Image References)
[dh_diagram]: ./images/dh_parameter.png

### Denavit-Hartenberg Diagram

Here is a Denavit-Hartenberg (DH) diagram of the Kuka KR16 L6:

![Denavit-Hartenberg diagram of the Kuka KR16 L6 6 DoF arm][dh_diagram]

The arm consists of six revolute joints connected in linear fashion.

### 📐 Denavit-Hartenberg Table

The following DH parameters are based on the physical specifications of the KUKA KR16 L6:

> All distances are in meters, angles in radians.

| Joint (n) | θ (theta) |    d    |    a    | α (alpha) |
|:---------:|:---------:|:-------:|:-------:|:---------:|
|     1     |  θ₁       |  0.675  |  0.260  |  -π/2     |
|     2     |  θ₂       |   0     |  0.680  |   0       |
|     3     |  θ₃       |   0     | -0.035  |  -π/2     |
|     4     |  θ₄       |  0.970  |   0     |   π/2     |
|     5     |  θ₅       |   0     |   0     |  -π/2     |
|     6     |  θ₆       |  0.115  |   0     |   0       |

- The `a` and `alpha` parameters are constant for each joint as they depend on the robot’s mechanical design.
- Only the `theta` parameters vary since all joints are revolute.

---

###  Inverse Kinematics (IK)

An **analytical geometric solution** is used to compute the joint angles required to reach a desired pose. This approach leverages the structure of the robot — especially the **spherical wrist configuration** — for simplification.

### IK Steps:
1. **Compute the wrist center**  
   Subtract the last link offset along the end-effector z-axis.

2. **Solve for first three joints (θ₁–θ₃)**  
   Use geometric and trigonometric relationships.

3. **Compute rotation from joint 3 to 6**  
   Derive the rotation matrix from base to wrist, then isolate wrist rotation.

4. **Solve for wrist joints (θ₄–θ₆)**  
   Extract angles from the wrist rotation matrix.

---

You can view the implementation in this file:  
👉 [Inverse Kinematics Implementation](./high_level_control/inverse_kinematics/ik_solver.py)

---

### Jacobian Matrix

This module computes the **Jacobian matrix** for the 6-DOF KUKA KR16 L6 robotic arm using its Denavit-Hartenberg parameters and forward kinematics.

The Jacobian relates joint velocities to the end-effector's linear and angular velocities, which is essential for motion control, singularity analysis, and velocity kinematics.

---

### Features

- Computes the **6×6 geometric Jacobian** (linear + angular velocity)
- Includes **singularity and conditioning checks**

---

You can view the implementation in this file:  
👉 [Jacobian Matrix Implementation](./high_level_control/jacobian/jacobian.py)


## Trajectory


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

