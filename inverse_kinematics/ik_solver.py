import numpy as np

POS_ERROR_THRESHOLD = 1e-3
ROT_ERROR_THRESHOLD = 1e-6

class InverseKinematicsSolver:
    def __init__(self, robot, px, py, pz, roll, pitch, yaw):
        self.robot = robot
        self.px, self.py, self.pz = px, py, pz
        self.roll, self.pitch, self.yaw = np.radians([roll, pitch, yaw])
        self.rot_ee = self.compute_rotation_matrix()
        self.wc = self.compute_wrist_center()

    def compute_rotation_matrix(self):
        Rz = np.array([[np.cos(self.yaw), -np.sin(self.yaw), 0],
                       [np.sin(self.yaw), np.cos(self.yaw), 0],
                       [0, 0, 1]])
        Ry = np.array([[np.cos(self.pitch), 0, np.sin(self.pitch)],
                       [0, 1, 0],
                       [-np.sin(self.pitch), 0, np.cos(self.pitch)]])
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(self.roll), -np.sin(self.roll)],
                       [0, np.sin(self.roll), np.cos(self.roll)]])
        return Rz @ Ry @ Rx

    def compute_wrist_center(self):
        return np.array([self.px, self.py, self.pz]) - self.robot.d7 * self.rot_ee[:, 2]

    def solve(self):
        r = self.robot
        WC = self.wc
        d1, d4, a1, a2 = r.d1, r.d4, r.a1, r.a2

        theta1_a = np.arctan2(WC[1], WC[0])
        theta1_b = theta1_a + np.pi
        side_b = np.sqrt((np.sqrt(WC[0]**2 + WC[1]**2) - a1)**2 + (WC[2] - d1)**2)
        side_a, side_c = d4, a2
        angle_a = np.arccos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c))
        angle_b = np.arccos((side_a**2 + side_c**2 - side_b**2) / (2 * side_a * side_c))

        theta2_a = np.pi/2 - angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
        theta3_a = np.pi/2 - (angle_b + 0.036)
        theta2_b = np.pi/2 + angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
        theta3_b = np.pi/2 - (-angle_b + 0.036)

        combinations = [
            (theta1_a, theta2_a, theta3_a),
            (theta1_a, theta2_b, theta3_b),
            (theta1_b, theta2_a, theta3_a),
            (theta1_b, theta2_b, theta3_b)
        ]

        valid_solutions = []
        for t1, t2, t3 in combinations:
            T0_1 = r.tf_matrix(0, 0, r.d1, t1)
            T1_2 = r.tf_matrix(-np.pi/2, r.a1, 0, t2 - np.pi/2)
            T2_3 = r.tf_matrix(0, r.a2, 0, t3)
            R0_3 = T0_1[:3, :3] @ T1_2[:3, :3] @ T2_3[:3, :3]
            R3_6 = R0_3.T @ self.rot_ee

            for sign in [1, -1]:
                theta5 = np.arctan2(sign * np.sqrt(R3_6[0, 2]**2 + R3_6[2, 2]**2), R3_6[1, 2])
                theta4 = np.arctan2(sign * R3_6[2, 2], -sign * R3_6[0, 2])
                theta6 = np.arctan2(-sign * R3_6[1, 1], sign * R3_6[1, 0])
                joint_angles = (t1, t2, t3, theta4, theta5, theta6)

                if self.is_within_limits(joint_angles):
                    is_valid, pos_err, rot_err = self.check_solution_error(joint_angles)
                    if is_valid:
                        valid_solutions.append((joint_angles, pos_err, rot_err))
        return valid_solutions

    def is_within_limits(self, thetas):
        return all(low <= angle <= high for angle, (low, high) in zip(thetas, self.robot.joint_limits))

    def check_solution_error(self, thetas):
        r = self.robot
        T0_1 = r.tf_matrix(0, 0, r.d1, thetas[0])
        T1_2 = r.tf_matrix(-np.pi/2, r.a1, 0, thetas[1] - np.pi/2)
        T2_3 = r.tf_matrix(0, r.a2, 0, thetas[2])
        T3_4 = r.tf_matrix(-np.pi/2, r.a3, r.d4, thetas[3])
        T4_5 = r.tf_matrix(np.pi/2, 0, 0, thetas[4])
        T5_6 = r.tf_matrix(-np.pi/2, 0, 0, thetas[5])
        T6_EE = r.tf_matrix(0, 0, r.d7, 0)
        T0_EE = T0_1 @ T1_2 @ T2_3 @ T3_4 @ T4_5 @ T5_6 @ T6_EE

        pos_err = np.linalg.norm(T0_EE[:3, 3] - np.array([self.px, self.py, self.pz]))
        rot_err = np.linalg.norm(T0_EE[:3, :3] - self.rot_ee)
        return pos_err < POS_ERROR_THRESHOLD and rot_err < ROT_ERROR_THRESHOLD, pos_err, rot_err
