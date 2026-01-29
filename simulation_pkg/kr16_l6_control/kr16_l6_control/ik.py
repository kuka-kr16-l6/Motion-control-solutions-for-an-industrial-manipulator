#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import time     

class IKPublisher(Node):
    def __init__(self):
        super().__init__('ik_publisher')
        self.publisher_ = self.create_publisher(JointTrajectory, "set_joint_trajectory", 10)

    def compute_joint_angles(self, px, py, pz, roll_deg, pitch_deg, yaw_deg):
        roll, pitch, yaw = np.radians([roll_deg, pitch_deg, yaw_deg])
        d1, d4, d7 = 0.675, 0.97, 0.115
        a1, a2, a3 = 0.26, 0.680, -0.035

        def TF_Matrix(alpha, a, d, q):
            c_q, s_q = np.cos(q), np.sin(q)
            c_a, s_a = np.cos(alpha), np.sin(alpha)
            return np.array([
                [c_q, -s_q, 0, a],
                [s_q * c_a, c_q * c_a, -s_a, -s_a * d],
                [s_q * s_a, c_q * s_a, c_a, c_a * d],
                [0, 0, 0, 1]
            ])

        ROT_EE = (
            np.array([[np.cos(yaw), -np.sin(yaw), 0],
                      [np.sin(yaw),  np.cos(yaw), 0],
                      [0, 0, 1]]) @
            np.array([[np.cos(pitch), 0, np.sin(pitch)],
                      [0, 1, 0],
                      [-np.sin(pitch), 0, np.cos(pitch)]]) @
            np.array([[1, 0, 0],
                      [0, np.cos(roll), -np.sin(roll)],
                      [0, np.sin(roll),  np.cos(roll)]])
        )

        WC = np.array([px, py, pz]) - d7 * ROT_EE[:, 2]
        theta1 = np.arctan2(WC[1], WC[0])

        side_a, side_c = d4, a2
        side_b = np.sqrt((np.sqrt(WC[0]**2 + WC[1]**2) - a1)**2 + (WC[2] - d1)**2)

        angle_a = np.arccos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c))
        angle_b = np.arccos((side_a**2 + side_c**2 - side_b**2) / (2 * side_a * side_c))

        theta2 = np.pi/2 - angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
        theta3 = np.pi/2 - (angle_b + 0.036)

        JOINT_LIMITS = [
            (-np.pi, np.pi),
            (-1.1344, 2.18166),
            (-3.8397, 1.117),
            (-6.1086, 6.1086),
            (-2.268, 2.268),
            (-6.1086, 6.1086)
        ]

        T0_1 = TF_Matrix(0, 0, d1, theta1)
        T1_2 = TF_Matrix(-np.pi/2, a1, 0, theta2 - np.pi/2)
        T2_3 = TF_Matrix(0, a2, 0, theta3)
        R0_3 = T0_1[:3, :3] @ T1_2[:3, :3] @ T2_3[:3, :3]
        R3_6 = R0_3.T @ ROT_EE

        theta4 = np.arctan2(R3_6[2, 2], -R3_6[0, 2])
        theta5 = np.arctan2(np.sqrt(R3_6[0, 2]**2 + R3_6[2, 2]**2), R3_6[1, 2])
        theta6 = np.arctan2(-R3_6[1, 1], R3_6[1, 0])

        joint_angles = [theta1, theta2, theta3, theta4, theta5, theta6]

        def is_within_limits(thetas):
            return all(low <= angle <= high for angle, (low, high) in zip(thetas, JOINT_LIMITS))

        if not is_within_limits(joint_angles):
            print("❌ Joint angles are out of limits.")
            return None

        return joint_angles


def main(args=None):
    rclpy.init(args=args)
    node = IKPublisher()

    try:
        while rclpy.ok():
            print("\n--- Inverse Kinematics Input ---")
            print("Type 'exit' at any time to quit.")

            pos_input = input("Enter position (px py pz): ")
            if pos_input.lower() == 'exit':
                break
            ori_input = input("Enter orientation (roll pitch yaw in degrees): ")
            if ori_input.lower() == 'exit':
                break

            try:
                px, py, pz = map(float, pos_input.strip().split())
                roll, pitch, yaw = map(float, ori_input.strip().split())
                joint_angles = node.compute_joint_angles(px, py, pz, roll, pitch, yaw)

                if joint_angles is not None:
                    msg = JointTrajectory()
                    msg.header.frame_id = "base_footprint"
                    msg.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]

                    point = JointTrajectoryPoint()
                    point.positions = joint_angles
                    point.time_from_start.sec = 1
                    msg.points.append(point)

                    node.publisher_.publish(msg)
                    node.get_logger().info(f"✅ Published joint angles (rad): {np.round(joint_angles, 2)}")
                rclpy.spin_once(node, timeout_sec=0.1)
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")
    except KeyboardInterrupt:
        print("👋 Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
