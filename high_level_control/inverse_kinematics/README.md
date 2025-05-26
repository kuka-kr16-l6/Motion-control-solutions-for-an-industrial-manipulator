[//]: # (Image References)
[dh_diagram]: ../../images/dh_parameter.png

# Denavit-Hartenberg Diagram

Here is a Denavit-Hartenberg (DH) diagram of the Kuka KR16 L6:

![Denavit-Hartenberg diagram of the Kuka KR16 L6 6 DoF arm][dh_diagram]

The arm consists of six revolute joints connected in linear fashion.

## Denavit-Hartenberg Table

Based on the arm's specifications, the following parameter were derived:

| n |  theta |   d   |    a   | alpha |
|:-:|:------:|:-----:|:------:|:-----:|
| 1 | theta1 | 0.675 |  0.26  | -pi/2 |
| 2 | theta2 |   0   |  0.68  |   0   |
| 3 | theta3 |   0   | -0.035 | -pi/2 |
| 4 | theta4 | 0.97  |    0   |  pi/2 |
| 5 | theta5 |   0   |    0   | -pi/2 |
| 6 | theta6 | 0.115 |    0   |   0   |

The a and alpha parameters do not change because they are specific to each arm. However, the theta and d parameters can change depending on the orientation of the arm. But for this arm, only the theta parameters will change since all the joints are revolute.


## Inverse Kinematics

To solve the inverse kinematics of the Kuka KR16 L6, a **geometric solution** approach was used. This method leverages the specific structure of the robot — particularly its spherical wrist configuration — to analytically derive joint angles based on the position and orientation of the end effector.

### Steps:
1. **Compute the wrist center**: Subtract the last link offset along the end-effector z-axis.
2. **Solve for first three joints (theta1–theta3)** using geometric relationships.
3. **Compute rotation from joint 3 to 6**.
4. **Solve for wrist orientation (theta4–theta6)** from the rotation matrix.

---

You can view the implementation in this file:  
👉 [Inverse Kinematics Implementation](./ik_solver.py)
