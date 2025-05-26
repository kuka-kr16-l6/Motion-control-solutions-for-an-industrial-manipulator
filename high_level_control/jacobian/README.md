# Jacobian Matrix – KUKA KR16 L6

This module computes the **Jacobian matrix** for the 6-DOF KUKA KR16 L6 robotic arm using its Denavit-Hartenberg parameters and forward kinematics.

The Jacobian relates joint velocities to the end-effector's linear and angular velocities, which is essential for motion control, singularity analysis, and velocity kinematics.

---

## 🧠 Features

- Computes the **6×6 geometric Jacobian** (linear + angular velocity)
- Includes **singularity and conditioning checks**

---

You can view the implementation in this file:  
👉 [Jacobian Matrix Implementation](./jacobian.py)
