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
5. [Simulation](#5-simulation)
6. [About the Team](#6-About-the-Team)

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
- FreeRTOS (built-in in ESP-IDF)  [FreeRTOS docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html)  
- ESP-Modbus library  [ESP-Modbus docs](https://docs.espressif.com/projects/esp-modbus/en/latest/esp32/)

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

* **see more References**:

  * [ESP-IDF Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/)
  * [Modbus RTU Protocol](https://modbus.org/)



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
  $$|q_j(t)| \le q_{max, j}$$

  **Velocity Limits:**
  $$|\dot{q}_j(t)| \le \dot{q}_{max, j}$$

  **Acceleration Limits:**
  $$|\ddot{q}_j(t)| \le \ddot{q}_{max, j}$$

![Optimized Joint Trajectories][Optimized_trajectory]

By decoding the PSO output back into the `FourierJoint` objects, we extract the optimal, physically safe excitation trajectory that guarantees the best possible parameter identification for the robot.

---
View implementation in:

👉 [View code](./high_level_control/dynamic_parameter_identification/pso.py)

---

## 5. Simulation
   ### Gazebo Simulation Package
   A complete Gazebo simulation environment for the KUKA KR16 L6 is provided. The simulation includes the robot model with proper joint configurations and URDF/Xacro files. It allows for testing and visualization of robot behavior in a virtual environment, aiding in development and validation before deployment on real hardware.
   For more details:
   [kr16_l6_pkg](./simulation_pkg/kr16_l6/)


   ### ROS 2 Control Package (Humble)
   A control package built using ROS 2 Humble is included to interface with the simulated or physical KUKA KR16 L6 robot. It provides essential ROS 2 nodes, launch files, and configurations for controlling the robot’s joints and executing motion commands. This package forms the foundation for integrating motion planning, feedback control, and autonomous behaviors.
   For more details:
   [kr16_l6_control](./simulation_pkg/kr16_l6_control/)

## 6. About the Team

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

