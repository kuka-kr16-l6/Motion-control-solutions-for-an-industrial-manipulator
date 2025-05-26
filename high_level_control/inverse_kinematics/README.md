[//]: # (Image References)
[dh_diagram]: ../../images/dh_parameter.png

# Denavit-Hartenberg Diagram

Here is a Denavit-Hartenberg (DH) diagram of the Kuka KR16 L6:

![Denavit-Hartenberg diagram of the Kuka KR16 L6 6 DoF arm][dh_diagram]

The arm consists of six revolute joints connected in linear fashion.

## 📐 Denavit-Hartenberg Table

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

## 🔁 Inverse Kinematics (IK)

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
👉 [Inverse Kinematics Implementation](./ik_solver.py)
