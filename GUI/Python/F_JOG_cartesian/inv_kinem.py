import numpy as np 
from .robot import robotRobot
POS_ERROR_THRESHOLD = 1e-3
ROT_ERROR_THRESHOLD = 1e-6

robot = robotRobot()

class InverseKinematicsSolver:
    def __init__(self, robot, px, py, pz, roll, pitch, yaw, previous_theta=None):
        self.robot = robot
        self.px, self.py, self.pz = px, py, pz
        self.roll, self.pitch, self.yaw = roll, pitch, yaw
        self.rot_ee = self.compute_rotation_matrix()
        self.wc = self.compute_wrist_center()
        self.previous_theta = previous_theta

    def compute_rotation_matrix(self):
        Rz = np.array([[np.cos(self.yaw), -np.sin(self.yaw), 0],
                       [np.sin(self.yaw),  np.cos(self.yaw), 0],
                       [0, 0, 1]])
        Ry = np.array([[np.cos(self.pitch), 0, np.sin(self.pitch)],
                       [0, 1, 0],
                       [-np.sin(self.pitch), 0, np.cos(self.pitch)]])
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(self.roll), -np.sin(self.roll)],
                       [0, np.sin(self.roll),  np.cos(self.roll)]])
        return Rz @ Ry @ Rx

    def compute_wrist_center(self):
        return np.array([self.px, self.py, self.pz]) - self.robot.d7 * self.rot_ee[:, 2]

    def solve(self):
        r = self.robot
        WC = self.wc
        d1, d4, a1, a2, a3 = r.d1, r.d4, r.a1, r.a2, r.a3

        theta1 = np.arctan2(WC[1], WC[0])

        side_a = np.sqrt(d4**2 + a3**2)   # repo: side_a = 1.501 (= sqrt(1.5**2 + 0.054**2))
        side_b = np.sqrt((np.sqrt(WC[0]**2 + WC[1]**2) - a1)**2 + (WC[2] - d1)**2)
        side_c = a2                        # repo: side_c = 1.25

        angle_a = np.arccos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c))
        angle_b = np.arccos((side_a**2 + side_c**2 - side_b**2) / (2 * side_a * side_c))

        offset = -np.arctan2(a3, d4)       # repo: hardcoded 0.036 for their a3=-0.054, d4=1.5

        theta2 = np.pi/2 - angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
        theta3 = np.pi/2 - (angle_b + offset)

        T0_1 = r.tf_matrix(0, 0, r.d1, theta1)
        T1_2 = r.tf_matrix(-np.pi/2, r.a1, 0, theta2 - np.pi/2)
        T2_3 = r.tf_matrix(0, r.a2, 0, theta3)
        R0_3 = T0_1[:3, :3] @ T1_2[:3, :3] @ T2_3[:3, :3]
        R3_6 = R0_3.T @ self.rot_ee

        theta4 = np.arctan2(R3_6[2, 2], -R3_6[0, 2])
        theta5 = np.arctan2(np.sqrt(R3_6[0, 2]**2 + R3_6[2, 2]**2), R3_6[1, 2])
        theta6 = np.arctan2(-R3_6[1, 1], R3_6[1, 0])

        joint_angles = (theta1, theta2, theta3, theta4, theta5, theta6)
        is_valid, pos_err, rot_err = self.check_solution_error(joint_angles)
        valid_solutions = [joint_angles] if (self.is_within_limits(joint_angles) and is_valid) else []

        return valid_solutions

    def get_best_solution(self):
        sols = self.solve()
        if not sols:    
            return None
        q_candidates = [np.array(sol, dtype=float) for sol in sols]
        # print("q_candidates:", np.rad2deg(q_candidates))
        if self.previous_theta is not None:
            reference_q = np.array(self.previous_theta, dtype=float)
        else:
            reference_q = np.zeros_like(q_candidates[0])
        
        min = 100 
        delta = 0
        for i, Q in enumerate(q_candidates):
            for j in range(len(Q)):
                delta = delta + abs((Q[j]-reference_q[j]))
            if delta < min :
                index  = i
                min = delta 
            delta = 0
        return q_candidates[index]

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

# def main():
#     solver = InverseKinematicsSolver(robot, 0.8459310470021182, 0.8467504760362499, 0.22849675595607463, np.deg2rad(-170.91648510612396), np.deg2rad(-26.858010241974384), np.deg2rad(26.121886655386525), None)
#     best_solution = solver.get_best_solution()
#     if best_solution is not None:
#         # print("Best solution (radians):", best_solution)
#         print("Best solution (degrees):", np.rad2deg(best_solution))
#     else:
#         print("No valid solution found.")

# if __name__ == "__main__":
#     main()