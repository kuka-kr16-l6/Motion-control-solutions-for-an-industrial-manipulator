# Robot Kinematics Model – KUKA KR16 L6

This module defines the kinematic structure of the **KUKA KR16 L6** robotic arm using the **Denavit-Hartenberg (DH)** convention.
It includes geometric parameters and a method to compute the homogeneous transformation matrix for each link.

---

## 🦾 Class: `Robot`

This class encapsulates the physical parameters of the 6-DOF KUKA KR16 L6 manipulator and provides a utility to generate transformation matrices based on DH parameters.

---

## 🧠 Features

- Defines full Denavit-Hartenberg parameters for the KUKA KR16 L6 robot

- Provides a method to compute the homogeneous transformation matrix for any link

- Includes joint limits for all 6 revolute joints

- Designed for easy integration with inverse kinematics, Jacobian computation, and simulation modules

- Lightweight and efficient using NumPy arrays for matrix operations

---

## 📄 Configuration Guide

For a complete breakdown of the kinematic model configuration, joint parameters, and transformation setup, refer to the documentation:

- [🔧 Robot Configuration Documentation (PDF)](../../hardware/mechanical/data/db_kr_16_l6_en.pdf)


This document supports the implementation and can help you verify or customize the DH model used in the code.


You can view the implementation in this file:  
👉 [Parameters Implementation](./robot.py)
