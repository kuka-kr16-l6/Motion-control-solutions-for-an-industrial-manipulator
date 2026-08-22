# KUKA KR16 L6 Control

## Table of content
1. [Introduction](#1-Introduction)
2. [Hardware](#2-Hardware)
    - [Mechanical](#mechanical)
    - [Electrical](#electrical)
3. [Low Level Control](#3-Low-Level-Control)
4. [High Level Control](#4-High-Level-Control)
    - [Kinematics](#kinematics)
    - [Path planning](#Path-planning)
    - [Trajectory](#Trajectory)
    - [Dynamic Parameter Identification](#parameter-identification)
5. [GUI](#5-gui)
6. [Simulation](#6-simulation)
7. [About the Team](#7-About-the-Team)

## 1. Introduction


This repository documents the development of both low-level and high-level control systems for the KUKA KR16 L6 industrial robotic arm. The objective is to integrate embedded hardware with advanced robotic motion planning, offering a comprehensive platform for real-time motor control, communication protocols, kinematic modeling, and trajectory planning.

Whether you're working on robotics research, industrial automation, or control systems education, this repository serves as a modular, scalable, and open starting point for working with 6-DOF industrial arms.

The project is designed to provide hands-on experience in:

- Low-level interfacing with industrial servo drives using microcontrollers and real-time operating systems (FreeRTOS)

- High-level motion control algorithms including forward/inverse kinematics and Jacobian computation

- Industrial communication via Modbus RTU over RS-485

- Practical implementation of control theory in a real robotic system

---

## 2. Hardware
A detailed PDF datasheet for the KUKA KR16 L6 robotic arm is included. It contains comprehensive technical specifications, including joint limits, reach, payload, accuracy, weight, and power requirements. This document serves as a reference for modeling, simulation, and control design.
[kr16_l6_datasheet](./data/MA_KR_6_16_en.pdf)

### Mechanical
A SolidWorks assembly model of the KUKA KR16 L6 robotic arm is included. This model provides an accurate representation of the robot’s external structure, suitable for visualization, workspace analysis, and physical integration planning. Please note that the model does not include internal mechanical or electrical components.
[SolidWorks assembly](./hardware/mechanical/solidworks_assembly/kr16_l6)

---

### Electrical
This PDF explains all the important details needed to build and connect the robot, control panel, and electronic components.
[wiring & schematics](./data/wiring&schematics.pdf)

#### Inside the Document

- **Motor & Driver Assignments**  
  Clear mapping of each axis (A1–A6) to its respective motor and driver.

- **Cable Specifications**  
  Encoder, brake, and servomotor cable types, connectors, part numbers, and manufacturers (e.g., DDK Ltd. CM10 series).

- **Control Panel Layout**  
  Visual reference for control box wiring, shield grounding, and power distribution.

- **Signal Mapping**  
  Detailed I/O pinouts for drivers, including input/output signal names and Yaskawa 50-pin to dual DB25 adapter configuration.

- **Custom PCB Schematics**  
  ESP-based board connections for pulse generation, encoder feedback, RS-485 communication, limit switches, and power rails.

- **Power & Safety Notes**  
  Includes voltage references, brake activation signals, grounding, and shielding requirements.

  ---

## 3. Low-Level Control

### Overview

The Low-Level Control layer is responsible for the real-time control of each joint of the KUKA KR16 L6 robotic arm.

Each joint is implemented as an independent control node based on the **STM32H743VIT6 (ARM Cortex-M7 @ 168 MHz)**. The joint controllers communicate with a centralized high-level controller through an **FDCAN bus using Classic CAN frames**.

The firmware is developed using **STM32CubeIDE** and STM32 **HAL/LL APIs**, with hardware peripherals used to achieve deterministic motor-control timing and fast safety response.

### Distributed System Architecture

The robotic arm uses a **distributed master–slave architecture**. The high-level controller is responsible for generating and distributing joint motion commands, while each STM32 node independently executes the commands for its assigned joint.

```text
                    ┌─────────────────────────┐
                    │    Master Controller    │
                    │                         │
                    │   High-Level Control    │
                    │   Trajectory Planning   │
                    └────────────┬────────────┘
                                 │
                         FDCAN / Classic CAN
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │   JOINT 1   │    │   JOINT 2   │    │   JOINT 6   │
       │ STM32H743   │    │ STM32H743   │    │ STM32H743   │
       │  Slave Node │    │  Slave Node │    │  Slave Node │
       └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │  SERVOPACK  │    │  SERVOPACK  │    │  SERVOPACK  │
       │    Driver   │    │    Driver   │    │    Driver   │
       └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
              │                  │                  │
              ▼                  ▼                  ▼
           Motor 1             Motor 2             Motor 6
```

Each joint has a unique `NODE_SLAVE_ID`, allowing incoming CAN messages to be filtered and processed only by their intended joint controller.

### Key Features

* Distributed control architecture with independent STM32 joint nodes
* **FDCAN communication** using Classic CAN frames
* Hardware-based **Pulse Train Output (PTO)** generation
* Microsecond-resolution motor-control timing
* Hardware **Quadrature Encoder Interface (QEI)** for position feedback
* Floating-point pulse-error accumulation to reduce trajectory drift
* FIFO-based motion-command buffering
* Hardware-driven safety fault handling
* Motor brake and servo-enable control
* Joint-specific gear-ratio and pulse-per-degree scaling
* Real-time encoder telemetry and RPM calculation

### Hardware Configuration

Each joint controller is based on the following hardware:

* **STM32H743VIT6**
* ARM Cortex-M7 running at **168 MHz**
* Yaskawa SERVOPACK motor driver
* Servo motor
* Incremental quadrature encoder
* FDCAN communication interface
* DAC outputs for current/torque reference
* Hardware brake and servo-enable signals

The main peripherals used by the firmware are:

| Peripheral | Function                                                 |
| ---------- | -------------------------------------------------------- |
| **TIM1**   | Pulse Train Output (PTO) generation                      |
| **TIM3**   | Quadrature Encoder Interface (QEI)                       |
| **FDCAN2** | Master–slave communication                               |
| **DAC1**   | Analog current/torque reference                          |
| **EXTI**   | Hardware safety/fault detection                          |
| **GPIO**   | Direction, brake, servo enable, clear and status signals |

### Pulse Train Generation

Motor pulses are generated using **TIM1 in One Pulse Mode (OPM)**.

The timer operates with a **1 MHz base clock**, providing a resolution of **1 µs per timer tick**. The pulse frequency is controlled through the timer Auto-Reload Register (ARR), while the number of pulses is configured using the repetition counter.

```text
Motion Command
      │
      ▼
Calculate Pulse Count
      │
      ▼
Calculate Pulse Frequency
      │
      ▼
Configure TIM1
      │
      ├── ARR → Pulse Frequency
      ├── CCR1 → 50% Duty Cycle
      └── RCR → Number of Pulses
      │
      ▼
Hardware PTO Generation
      │
      ▼
Servo Driver
```

This hardware-based approach allows the STM32 to generate accurate pulse trains without relying on software delays or CPU-based timing.

### Encoder Interface

**TIM3** is configured as a hardware **Quadrature Encoder Interface (QEI)** using X4 encoder mode.

The encoder signals are connected to:

* `PA6` → TIM3 Channel 1
* `PA7` → TIM3 Channel 2

The encoder counter is used to track the actual joint movement and provides the basis for position verification and real-time velocity calculation.

### Motion Command Processing

Incoming CAN commands are decoded by the FDCAN receive interrupt and converted into internal motion commands.

```text
FDCAN Frame
     │
     ▼
Decode Command
     │
     ├── Direction
     ├── Target Angle
     └── Target Speed
     │
     ▼
Servo_Push_Command()
     │
     ▼
Pulse Calculation
     │
     ▼
Motion Command FIFO
     │
     ▼
TIM1 PTO Execution
```

The command FIFO allows incoming motion commands to be buffered while the hardware timer is executing the current command. This enables continuous multi-segment motion without blocking CAN reception.

### Pulse Error Accumulation

The firmware uses a **floating-point pulse-error accumulation algorithm** to prevent positional drift caused by converting fractional pulse values into integer pulse counts.

For each command:

```text
Target Angle
     │
     ▼
Angle × Pulses/Degree
     │
     ▼
Add Previous Error
     │
     ▼
Integer Pulse Count
     │
     ├──────────────► TIM1
     │
     ▼
Store Fractional Remainder
     │
     ▼
Next Motion Command
```

The remaining fractional pulse value is carried into the next motion command. This preserves the accumulated position over multiple trajectory segments instead of independently rounding every command.

### FDCAN Communication

The communication interface uses **FDCAN2** configured for **Classic CAN with standard 11-bit identifiers**.

The physical interface uses:

* `PB5` → FDCAN RX
* `PB6` → FDCAN TX

#### Master → Joint Command

Each motion command contains:

| Field       |    Size | Description           |
| ----------- | ------: | --------------------- |
| `dir`       |  1 byte | Direction of rotation |
| `angle_deg` | 4 bytes | Target angle × 1000   |
| `speed_rpm` | 2 bytes | Target speed in RPM   |
| `unused`    |  1 byte | Padding               |

#### Joint → Master Feedback

The joint controller can return:

| Field       |    Size | Description                    |
| ----------- | ------: | ------------------------------ |
| `dir`       |  1 byte | Current/last direction         |
| `angle_deg` | 4 bytes | Encoder angle × 100            |
| `speed_rpm` | 2 bytes | Calculated real-time RPM       |
| `status`    |  1 byte | Operational/status information |

This provides a bidirectional communication path between the high-level controller and the individual joint controllers.

### Safety Architecture

Safety handling is implemented using a **hardware-driven EXTI interrupt** connected to the servo driver's ready/fault signal.

```text
Servo Driver Fault
        │
        ▼
   PB12 / EXTI
        │
        ▼
Servo_Fault_Handler()
        │
        ├── Engage Motor Brake
        ├── Disable Servo Output
        ├── Stop TIM1 PTO
        ├── Clear Command FIFO
        └── Reset Pulse Error
```

When a driver fault or unsafe condition is detected, the firmware immediately stops pulse generation, disables the motor output, engages the mechanical brake, and clears pending motion commands.

This prevents previously queued commands from being executed after a fault condition.

### Joint-Specific Motion Scaling

Because the robot joints have different mechanical gear ratios and pulse requirements, each joint uses its own motion-scaling parameters.

| Joint   | Gear Ratio | Pulses/Degree | Base Speed |
| ------- | ---------: | ------------: | ---------: |
| Joint 1 |      125.0 |          2000 |    96.0 Hz |
| Joint 2 |      125.0 |          2000 |    96.0 Hz |
| Joint 3 |      125.0 |          2000 |    96.0 Hz |
| Joint 4 |     74.444 |          2010 |  161.99 Hz |
| Joint 5 |     42.222 |          1900 |   270.0 Hz |
| Joint 6 |     24.117 |          1900 |  472.69 Hz |

The firmware uses these parameters to translate high-level angular commands into the appropriate pulse count and pulse frequency for each joint.

### Firmware Flow

```text
Power ON
   │
   ▼
Initialize STM32 Peripherals
   │
   ├── TIM1
   ├── TIM3
   ├── DAC1
   └── FDCAN2
   │
   ▼
Servo Initialization
   │
   ▼
Enable FDCAN RX Interrupt
   │
   ▼
Wait for CAN Command
   │
   ▼
Decode Motion Command
   │
   ▼
Calculate Pulses & Frequency
   │
   ▼
Push Command to FIFO
   │
   ▼
TIM1 PTO Execution
   │
   ▼
Encoder Verification
   │
   ▼
Send Joint Feedback
   │
   └──────────────► Wait for Next Command
```

At any point during operation, a hardware fault can interrupt the normal execution flow and transfer control to the safety handler.

### Performance Validation

The architecture has been validated through experimental testing of both positional accuracy and real-time response.

The pulse-error accumulation algorithm achieved **zero cumulative positional drift** over a 1000-segment trajectory in the documented test, compared with significant accumulated error when fractional pulses were independently truncated.

The measured latency from FDCAN reception to the first physical PTO pulse was **14.2 µs**, while the measured safety-stop propagation from fault assertion to brake activation was **1.8 µs**.

### Running & Testing

The firmware is deployed directly on the **STM32H743VIT6 joint-controller hardware**.

Testing includes:

* FDCAN communication
* Motion-command reception
* Pulse generation
* Motor movement
* Encoder feedback
* Multi-segment trajectory execution
* Pulse-error accumulation
* Driver fault handling
* Emergency/safety stopping

### Source Code

The low-level controller implementation is located in the project repository under the low-level firmware source directory.

The main components include:

* `Robot_Joint.h/.c` — Joint-control API and motion/PTO implementation
* `FDCAN.c` — CAN communication and command decoding
* `main.c` — System initialization and application flow
  
### Future Scope

Planned extensions include:

* **Closed-Loop Position Control:** Implement a real-time PID position controller on the STM32 using TIM3 encoder feedback to improve joint positioning accuracy.

* **Velocity Control:** Extend the motor-control architecture to support velocity-based control using encoder feedback.

* **Encoder Feedback:** Transmit real-time encoder position and joint-state information from the STM32 controllers to the Raspberry Pi 5 for monitoring and high-level control.

* **CAN-Based Firmware Update Bootloader:** Develop a bootloader that uses the existing CAN bus to transfer firmware images from the Raspberry Pi 5 to individual STM32 joint controllers, enabling remote firmware updates without physical programming access.

* **micro-ROS Integration:** Investigate micro-ROS integration to connect the STM32 low-level controllers with the ROS 2 ecosystem running on the Raspberry Pi 5.

* **High-Speed FDCAN:** Evaluate the use of higher-speed FDCAN data transmission to increase communication bandwidth and support faster exchange of joint commands and feedback.

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

- [🔧 Robot Configuration Documentation (PDF)](./data/db_kr_16_l6_en.pdf)


This document supports the implementation and can help you verify or customize the DH model used in the code.


You can view the python implementation in this file:  
👉 [Parameters Implementation](./high_level_control/kinematics/python/parameters/robot.py)

You can view the cpp implementation in this file:  
👉 [Parameters Implementation](./high_level_control/kinematics/cpp/kinematics/Robot.h)

[//]: # (Image References)
[dh_diagram]: ./images/dh_parameter.png
[Optimized_trajectory]: ./images/optimized_trajectory.png
[PSO_BEFORE]: ./images/pso_1.png
[PSO_AFTER]: ./images/pso_2.png
[GUI]: ./images/gui.jpeg

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

You can view the python implementation in this file:  
👉 [Inverse Kinematics Implementation](./high_level_control/kinematics/python/inverse_kinematics/ik_solver.py)

------

You can view the cpp implementation in this file:  
👉 [Inverse Kinematics Implementation](./high_level_control/kinematics/cpp/kinematics/solve_ik.cpp)

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

---

## Path planning 
This section compute the points for collision free path 

### Sampling-based path planning

#### Rapidly-exploring random tree RRT
Sampling-based path planning method visualized in 3D space for collision-free motion.
![visualization for RRT in 3D space][RRT]

---
View implementaion in:

👉 [View code](./high_level_control/path_planner/RandomRapidlyExploringTrees.py)

---

### Search-based path planning

---

[LSWB]: ./images/LSWB.png
[Quintic polynomial]: ./images/QuinticPolynomial.png
[RRT]: ./images/RRT.png

## Trajectory  
In this section, position, velocity, and acceleration for each joint are computed using various methods to ensure smooth motion

  ### Point-to-point trajectory
  #### Linear segments with parabolic blends trajectory
Smooth transitions between joint positions using linear segments and acceleration-limited parabolic blends

![position, velocity, and acceleration for each joint using LSWB][LSWB]

---
View implementaion in:

👉 [View code](./high_level_control/trajectory/linearWblends_trajectory.py)

---

  #### Quintic polynomial trajectory
Ensures smooth motion with continuous acceleration and jerk profiles for precise joint-level movement.

![position, velocity, and acceleration for each joint using Quintic polynomial][Quintic polynomial]

---
View implementaion in:

👉 [View code](./high_level_control/trajectory/quinticPoly_traj.py)

---

  ### Trajectory with via points 

---
## Parameter Identification

This section describes the formulation and implementation of **parameter identification for robot dynamics** using a **linear-in-parameters regressor representation**.  
The goal is to obtain a minimal and identifiable set of dynamic parameters suitable for modeling, control, and simulation.

The symbolic derivation of the dynamic model, regressor matrix, and minimal parameter set is carried out using **SymPyBotics**, a Python toolbox for symbolic robot modeling and dynamics:

[SymPyBotics GitHub](https://github.com/cdsousa/SymPyBotics)

---

### Dynamic Model and Regressor Formulation

The rigid-body dynamics of an $n$-DOF robot manipulator can be written as:

$$
\tau(q, \dot{q}, \ddot{q}) = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + g(q)
$$

This nonlinear dynamic model can be rewritten in a **linear form with respect to the parameters**:

$$
\tau = Y(q, \dot{q}, \ddot{q}) \beta
$$

where:
- $Y(q, \dot{q}, \ddot{q})$ is the **regressor matrix**
- $\beta$ is the vector of **dynamic parameters**
- $q, \dot{q}, \ddot{q}$ are joint position, velocity, and acceleration vectors

All nonlinearities in the dynamics are captured by the regressor matrix, while the unknown physical parameters appear linearly in the parameter vector.

---

### Regressor Function

The regressor function computes the matrix:

$$
Y = f(q, \dot{q}, \ddot{q})
$$

Each row of $Y$ corresponds to one joint torque equation, and each column corresponds to a physical parameter or a combination of parameters, such as:
- Link masses  
- Center of mass locations  
- Inertia tensor components  
- Motor or friction parameters (if included)

This formulation enables the use of **linear least squares–based identification methods**, since the dynamic model is linear with respect to the unknown parameters.

However, the full regressor matrix generally contains **linearly dependent columns**, meaning that **not all parameters are independently identifiable**. These dependencies arise from the structure of rigid-body dynamics and the chosen parameterization. As a result, multiple parameter vectors may produce identical joint torques.

To address this issue, the regressor can be reduced to a **minimum (base) regressor**, which contains only linearly independent parameter combinations. The corresponding **base parameter vector** represents the smallest set of parameters that fully describes the robot dynamics.

The reduction to minimum parameters follows the methodology introduced by **Wisama Khalil**, where systematic techniques are used to:
- Detect linear dependencies in the regressor matrix  
- Eliminate redundant parameters  
- Construct a reduced regressor that preserves the dynamic behavior of the system  

This minimum-parameter formulation improves numerical conditioning, ensures physical consistency, and is essential for reliable parameter identification, especially when working with experimental data.

The referenced Khalil research paper included in this repository provides the theoretical foundation and practical procedure for minimizing the parameter set used in the regressor-based identification framework:  
[Identification of the minimum inertial parameters of robots](./data/identification-of-the-minimum-inertial-parameters-of-robots.pdf)

---
View implementation in:

👉 [View code](./high_level_control/dynamic_parameter_identification/regressor_base.py)

---

### Parameter Vector ($\beta$)

The parameter vector $\beta$ stacks all dynamic parameters appearing in the robot model (e.g., link masses, first moments, and inertia terms) and is defined such that the dynamics are linear in these parameters.  
The structure and ordering of $\beta$ are strictly consistent with the columns of the regressor matrix $Y$.

👉 [View code](./high_level_control/dynamic_parameter_identification/base_params_beta.py)

---
### Excitation Trajectory Generation

To accurately estimate the dynamic parameters (base parameter vector $\beta$), the robot must execute an **excitation trajectory**. This trajectory must persistently excite all the dynamics of the KUKA KR16 L6 across its workspace while remaining continuous and smooth to prevent mechanical damage.

We use a **Finite Fourier Series** to generate this periodic trajectory. By defining the Fourier series at the velocity level $\dot{q}(t)$ and deriving position $q(t)$ and acceleration $\ddot{q}(t)$ through integration and differentiation, we naturally prevent velocity drift.

For each joint $j$, the trajectory is parameterized by a fundamental frequency $\omega_f$, the number of harmonics $N_f$, an initial position offset $q_{0,j}$, and coefficient vectors $a_j$ and $b_j$:

**Joint Velocity:**

$$
\dot{q}_j(t) = \sum_{l=1}^{N_f} \left( a_{l,j} \cos(\omega_f l t) + b_{l,j} \sin(\omega_f l t) \right)
$$

**Joint Position:**

$$
q_j(t) = q_{0,j} + \sum_{l=1}^{N_f} \left( \frac{a_{l,j}}{\omega_f l} \sin(\omega_f l t) - \frac{b_{l,j}}{\omega_f l} \cos(\omega_f l t) \right)
$$

**Joint Acceleration:**

$$
\ddot{q}_j(t) = \sum_{l=1}^{N_f} \left( -a_{l,j} \omega_f l \sin(\omega_f l t) + b_{l,j} \omega_f l \cos(\omega_f l t) \right)
$$

This ensures that $q$, $\dot{q}$, and $\ddot{q}$ are strictly continuous, making it ideal for experimental data collection.
---
View implementation in:

👉 [View code](./high_level_control/dynamic_parameter_identification/excitation_trajectory.py)

---
### Trajectory Optimization via PSO

Generating a random Fourier series is not sufficient for parameter identification. If the trajectory does not adequately excite specific joints, the resulting regressor matrix $Y$ will be ill-conditioned, making the least-squares estimation highly sensitive to sensor noise.

To solve this, we optimize the Fourier coefficients to minimize the **Condition Number** $\kappa$ of the base regressor matrix $Y_B$. A lower condition number ensures maximum robustness against measurement noise in the torque and position sensors.

#### What is Particle Swarm Optimization (PSO)?
Since minimizing the condition number is a highly non-linear, non-convex optimization problem, we utilize **Particle Swarm Optimization (PSO)**. 

PSO is a computational algorithm inspired by the flocking behavior of birds. Instead of a single point systematically searching the space, a "swarm" of particles (potential solutions) is initialized randomly. Each particle explores the space and adjusts its position based on three factors:
1. **Inertia:** Its resistance to changing its current direction.
2. **Cognitive Pull:** Its memory of the best solution it has personally found ($p_{best}$).
3. **Social Pull:** Its communication with the swarm to move toward the absolute best solution found by anyone ($g_{best}$).

![PSO Convergence][PSO_BEFORE]
![PSO Convergence][PSO_AFTER]

**Optimization Problem Setup:**
* **Decision Variables ($x$):** The swarm optimizes a flat vector containing the parameters for all 6 joints. For each joint, the parameters are $[a_1 ... a_{N_f}, b_1 ... b_{N_f}, q_0]$.
* **Objective Function:** Minimize $J = \text{cond}(Y_B(x)) = \| Y_B \| \cdot \| Y_B^\dagger \|$
* **Constraints (Penalty Functions):**
* **Constraints (Penalty Functions):**
  During the PSO search, any particle (trajectory) that exceeds the KUKA KR16 L6's physical limits is heavily penalized:

**Position Limits:**

$$
|q_j(t)| \le q_{max, j}
$$

**Velocity Limits:**

$$
|\dot{q}_j(t)| \le \dot{q}_{max, j}
$$

**Acceleration Limits:**

$$
|\ddot{q}_j(t)| \le \ddot{q}_{max, j}
$$
  
![Optimized Joint Trajectories][Optimized_trajectory]

By decoding the PSO output back into the `FourierJoint` objects, we extract the optimal, physically safe excitation trajectory that guarantees the best possible parameter identification for the robot.

---
View implementation in:

👉 [View code](./high_level_control/dynamic_parameter_identification/pso.py)

---

## 5. GUI


A **Qt / QML desktop application** for jogging and controlling the KUKA KR16 L6 arm, with a Python (PySide6) backend that computes forward/inverse kinematics and quintic trajectories and streams motion commands to the robot over a **CAN bus**.

![GUI_Running_real][GUI]



The UI displays a live 3D model of the manipulator (imported from CAD via Qt Quick 3D) alongside joint- and cartesian-space jog controls, so an operator can move the arm either joint-by-joint or by driving the end-effector's X/Y/Z/roll/pitch/yaw directly.

### Features

- **Interactive 3D visualization** — the six links (`A1`–`A6`) and base of the manipulator are rendered as a Qt Quick 3D scene, imported from `.glb` CAD models, and pose is updated live as the arm moves.
- **Joint jog control** — six sliders/spin boxes (`joint1Angle`…`joint6Angle`) send target angles to the backend, which plans a smooth motion between the current and target pose.
- **Cartesian jog control** — six spin boxes for end-effector `X, Y, Z, Roll, Pitch, Yaw`; the backend solves inverse kinematics and drives the joints to reach the requested pose.
- **Multi-point Cartesian paths** — `executeMultipoint()` accepts a list of cartesian waypoints and generates a smooth B-spline path through them.
- **Quintic (5th-order polynomial) trajectory planning** — velocity- and acceleration-limited joint trajectories for smooth, jerk-free motion, with per-joint gear-ratio scaling.
- **Forward/Inverse Kinematics** — closed-form FK/IK based on Denavit–Hartenberg parameters for the KR16 L6, including joint-limit checking.
- **CAN bus communication** — `CanInterface` brings up a SocketCAN interface (default `can0` @ 500 kbit/s), packs each joint's direction/position/velocity into a CAN frame, and streams it to the robot controller during trajectory playback, with automatic reconnect on bus-off/error.
- **Live connection status indicator** in the UI (disconnected / connected / sending).
- **Debounced input handling** so rapid slider movement doesn't flood the bus with redundant motion commands.
- **Multi-language support** scaffolding (`i18n/`) for the QML UI.

### Repository structure

```
.
├── App/                        # Qt/C++ application shell (QQmlApplicationEngine bootstrap)
│   └── main.cpp
├── Python/                     # PySide6 backend — the actual application logic
│   ├── main.py                 # Backend QObject exposed to QML as `backend`
│   ├── F_communication/
│   │   └── can_interface.py    # SocketCAN interface (PySide6 QtSerialBus)
│   ├── F_JOG_joint/
│   │   ├── forward_kinem.py    # DH-based forward kinematics
│   │   └── quintic_traj.py     # Quintic joint-space trajectory generator
│   ├── F_JOG_cartesian/
│   │   ├── robot.py            # Robot model, DH params, joint limits
│   │   ├── inv_kinem.py        # Inverse kinematics
│   │   ├── inverse_J.py        # Jacobian-based IK helper
│   │   ├── quintic_cart.py     # Cartesian-space quintic trajectory
│   │   └── main_JOG_cart.py    # Cartesian jog trajectory orchestration
│   ├── F_CART_/                # Multi-point Cartesian path planning (B-spline)
│   │   ├── b_spline.py
│   │   ├── rmf_orientation.py
│   │   └── _main_cart_.py
│   └── autogen/                # Qt/QML environment bootstrap (generated by Qt Design Studio)
├── UntitledProject1/            # QML application module (event models, constants)
├── UntitledProject1Content/     # Main QML UI (App.qml, Screen01, Kuka_mainscreen, images, fonts)
├── Generated/QtQuick3D/         # Imported 3D robot link meshes (A1–A6, Base) as Qt Quick 3D components
├── Dependencies/                # Qt Design Studio component/import libraries (vendored)
├── i18n/                        # Translation files
├── cmake/, CMakeLists.txt*      # CMake build files for the C++/QML shell
└── UntitledProject1.qmlproject  # Qt Design Studio project file
```

> Note: this project was authored in **Qt Design Studio**, so several folders (`Dependencies/`, `Generated/`, `UntitledProject1*`, `cmake/`, `qds.cmake`) are studio-managed scaffolding rather than hand-written application code. The core logic lives in `Python/` (kinematics, trajectory planning, CAN communication) and `UntitledProject1Content/` (the UI).

### How it works

1. **`Python/main.py`** defines a `Backend` `QObject` that is exposed to QML as the context property `backend`. It holds the robot's current joint angles and cartesian pose.
2. The QML UI (`UntitledProject1Content/App.qml`) binds jog sliders to `backend.jointChanged(joint, angle)` and `backend.posChanged(axis, value)`.
3. On a joint move, `quintic_traj.py` generates a time-parameterized, velocity/acceleration-limited trajectory between the current and target joint angles.
4. On a cartesian move, `forward_kinem.py` / the `F_JOG_cartesian` inverse-kinematics solver compute the joint targets needed to reach the requested pose, then a trajectory is generated the same way.
5. At each trajectory step, the backend computes a direction, position delta, and velocity for every joint, packs them into a CAN frame per joint ID, and sends them via `CanInterface.send_all_joints()` over SocketCAN.
6. The 3D scene and cartesian read-outs are kept in sync with the live joint angles (forward kinematics is recomputed after every move).

### Requirements

- **Python 3.12+**
- **PySide6** (Qt for Python), including the `QtSerialBus` module for CAN communication
- **NumPy**
- A Linux host with **SocketCAN** support (`can0` interface) and a CAN adapter wired to the robot's joint controllers — or comment out/stub `CanInterface` to run the UI/kinematics without physical hardware
- **Qt Design Studio 4.8+ / Qt 6.8** if you want to edit the QML UI or 3D scene in the design tool
- (Optional, for the C++ shell in `App/`) **CMake** and a Qt 6 development environment

### Getting started

```bash
cd GUI-for-KUKA-6-DoF-manipulator/Python

# Install dependencies
pip install PySide6 numpy

# Run the application
python main.py
```
---

## 6. Simulation
   ### Gazebo Simulation Package
   A complete Gazebo simulation environment for the KUKA KR16 L6 is provided. The simulation includes the robot model with proper joint configurations and URDF/Xacro files. It allows for testing and visualization of robot behavior in a virtual environment, aiding in development and validation before deployment on real hardware.
   For more details:
   [kr16_l6_pkg](./simulation_pkg/kr16_l6/)


   ### ROS 2 Control Package (Humble)
   A control package built using ROS 2 Humble is included to interface with the simulated or physical KUKA KR16 L6 robot. It provides essential ROS 2 nodes, launch files, and configurations for controlling the robot’s joints and executing motion commands. This package forms the foundation for integrating motion planning, feedback control, and autonomous behaviors.
   For more details:
   [kr16_l6_control](./simulation_pkg/kr16_l6_control/)

## 7. About the Team

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

