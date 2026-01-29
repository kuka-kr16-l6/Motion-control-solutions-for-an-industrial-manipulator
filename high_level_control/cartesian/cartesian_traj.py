import numpy as np 
import matplotlib.pyplot as plt
import time


position_change = np.array([[0.5,1],[0.5,1],[0.5,1],[0,0],[0,0],[0,0]])
max_acceleration = 10
max_velocity = 10 

def time_calc(states , max_acceleration, max_velocity, alpha):
    max_time=[]
    for state in states:
        delta_theta = np.abs(state[1]-state[0])
        time_acc = np.sqrt((delta_theta) /(max_acceleration*alpha*(1-alpha)))
        time_velo = delta_theta / (max_velocity * (1 - alpha))
        max_time.append(max(time_acc,time_velo))
        
    print("time is :", max(max_time))
    return max(max_time)


def linear_blends_generator ( states , time , alpha):

    
    timesteps = np.linspace(0,time,100)
    ta = time * alpha
    tb = time - (ta)
    position_profile = []
    velocity_profile = []
    acceleration_profile = []

    for state in states:
        start_theta = state[0]
        end_theta = state[1]
        parabola_acceleration = (end_theta - start_theta) / (ta * (time - ta))
        position = []
        velocity = []
        acceleration = []

        for timestep in timesteps:
            if timestep < ta:
                position.append(start_theta + (parabola_acceleration*0.5*(timestep**2) ))
                velocity.append(parabola_acceleration*timestep)
                acceleration.append(parabola_acceleration)

            elif timestep >= ta and timestep <tb:
                position.append(start_theta + (parabola_acceleration*0.5*(ta**2) ) + parabola_acceleration * ta *(timestep - ta))
                velocity.append(parabola_acceleration * ta)
                acceleration.append(0)
            
            else :
                position.append(end_theta - (parabola_acceleration*0.5*(time -timestep)**2  ))
                velocity.append(parabola_acceleration*(time-timestep))
                acceleration.append(-parabola_acceleration)


        position_profile.append(position)
        velocity_profile.append(velocity)
        acceleration_profile.append(acceleration)

    return position_profile, velocity_profile, acceleration_profile



time = time_calc(position_change,max_acceleration, max_velocity, 0.3 )
position_profile, velocity_profile, acceleration_profile = linear_blends_generator(position_change, time, 0.3)
# print(position_profile)
angles_deg =[]


for i in range(len(position_profile[0])):
    # User input
    px, py, pz = position_profile[0][i], position_profile[1][i], position_profile[2][i]
    roll, pitch, yaw = [30, 40, 50]  
    roll, pitch, yaw = np.radians([roll, pitch, yaw])


    # Robot parameters
    d1, d4, d7 = 0.675, 0.97, 0.115
    a1, a2, a3 = 0.26, 0.680, -0.035

    # Joint limits (in radians)
    JOINT_LIMITS = [
        (-np.pi, np.pi),           # Joint 1
        (-1.1344, 2.18166),        # Joint 2
        (-3.8397, 1.117),          # Joint 3
        (-6.1086, 6.1086),         # Joint 4
        (-2.268, 2.268),           # Joint 5
        (-6.1086, 6.1086)          # Joint 6
    ]

    def TF_Matrix(alpha, a, d, q):
        c_q, s_q = np.cos(q), np.sin(q)
        c_a, s_a = np.cos(alpha), np.sin(alpha)
        return np.array([
            [c_q, -s_q, 0, a],
            [s_q * c_a, c_q * c_a, -s_a, -s_a * d],
            [s_q * s_a, c_q * s_a, c_a, c_a * d],
            [0, 0, 0, 1]
        ])

    # Compute end-effector rotation matrix
    ROT_EE = (
        np.array([[np.cos(yaw), -np.sin(yaw), 0],
                [np.sin(yaw), np.cos(yaw), 0],
                [0, 0, 1]]) @
        np.array([[np.cos(pitch), 0, np.sin(pitch)],
                [0, 1, 0],
                [-np.sin(pitch), 0, np.cos(pitch)]]) @
        np.array([[np.cos(yaw), -np.sin(yaw), 0],
                [np.sin(yaw), np.cos(yaw), 0],
                [0, 0, 1]]) 
    )

    # Wrist center
    WC = np.array([px, py, pz]) - d7 * ROT_EE[:, 2]

    # Theta1 possibilities
    theta1_a = np.arctan2(WC[1], WC[0])
    theta1_b = theta1_a + np.pi

    # Geometry for theta2/theta3
    side_a, side_c = d4, a2
    side_b = np.sqrt((np.sqrt(WC[0]**2 + WC[1]**2) - a1)**2 + (WC[2] - d1)**2)

    angle_a = np.arccos((side_b**2 + side_c**2 - side_a**2) / (2 * side_b * side_c))
    angle_b = np.arccos((side_a**2 + side_c**2 - side_b**2) / (2 * side_a * side_c))

    theta2_a = np.pi/2 - angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
    theta3_a = np.pi/2 - (angle_b + 0.036)
    theta2_b = np.pi/2 + angle_a - np.arctan2(WC[2] - d1, np.sqrt(WC[0]**2 + WC[1]**2) - a1)
    theta3_b = np.pi/2 - (-angle_b + 0.036)

    # All combinations
    theta_combinations = [
        (theta1_a, theta2_a, theta3_a),
        (theta1_a, theta2_b, theta3_b),
        (theta1_b, theta2_a, theta3_a),
        (theta1_b, theta2_b, theta3_b)
    ]

    all_solutions = []

    for theta1, theta2, theta3 in theta_combinations:
        T0_1 = TF_Matrix(0, 0, d1, theta1)
        T1_2 = TF_Matrix(-np.pi/2, a1, 0, theta2 - np.pi/2)
        T2_3 = TF_Matrix(0, a2, 0, theta3)
        R0_3 = T0_1[:3, :3] @ T1_2[:3, :3] @ T2_3[:3, :3]

        R3_6 = R0_3.T @ ROT_EE

        theta5_1 = np.arctan2(np.sqrt(R3_6[0, 2]**2 + R3_6[2, 2]**2), R3_6[1, 2])
        theta5_2 = np.arctan2(-np.sqrt(R3_6[0, 2]**2 + R3_6[2, 2]**2), R3_6[1, 2])

        theta4_1 = np.arctan2(R3_6[2, 2], -R3_6[0, 2])
        theta6_1 = np.arctan2(-R3_6[1, 1], R3_6[1, 0])

        theta4_2 = np.arctan2(-R3_6[2, 2], R3_6[0, 2])
        theta6_2 = np.arctan2(R3_6[1, 1], -R3_6[1, 0])

        all_solutions.append((theta1, theta2, theta3, theta4_1, theta5_1, theta6_1))
        all_solutions.append((theta1, theta2, theta3, theta4_2, theta5_2, theta6_2))

    POS_ERROR_THRESHOLD = 1e-3
    ROT_ERROR_THRESHOLD = 1e-6

    def is_within_limits(thetas):
        return all(low <= angle <= high for angle, (low, high) in zip(thetas, JOINT_LIMITS))

    def check_solution_error(thetas, target_pos, target_rot):
        t1, t2, t3, t4, t5, t6 = thetas

        T0_1 = TF_Matrix(0, 0, d1, t1)
        T1_2 = TF_Matrix(-np.pi/2, a1, 0, t2 - np.pi/2)
        T2_3 = TF_Matrix(0, a2, 0, t3)
        T3_4 = TF_Matrix(-np.pi/2, a3, d4, t4)
        T4_5 = TF_Matrix(np.pi/2, 0, 0, t5)
        T5_6 = TF_Matrix(-np.pi/2, 0, 0, t6)
        T6_EE = TF_Matrix(0, 0, d7, 0)

        T0_EE = T0_1 @ T1_2 @ T2_3 @ T3_4 @ T4_5 @ T5_6 @ T6_EE
        pos_err = np.linalg.norm(T0_EE[:3, 3] - target_pos)
        rot_err = np.linalg.norm(T0_EE[:3, :3] - target_rot)

        return pos_err < POS_ERROR_THRESHOLD and rot_err < ROT_ERROR_THRESHOLD, pos_err, rot_err

# def compute_jacobian(thetas):
#     t1, t2, t3, t4, t5, t6 = thetas
#     T0_1 = TF_Matrix(0, 0, d1, t1)
#     T1_2 = TF_Matrix(-np.pi/2, a1, 0, t2 - np.pi/2)
#     T2_3 = TF_Matrix(0, a2, 0, t3)
#     T3_4 = TF_Matrix(-np.pi/2, a3, d4, t4)
#     T4_5 = TF_Matrix(np.pi/2, 0, 0, t5)
#     T5_6 = TF_Matrix(-np.pi/2, 0, 0, t6)
#     T6_EE = TF_Matrix(0, 0, d7, 0)

#     T_matrices = [T0_1, T1_2, T2_3, T3_4, T4_5, T5_6, T6_EE]
#     T_cumul = [np.eye(4)]
#     for T in T_matrices:
#         T_cumul.append(T_cumul[-1] @ T)
#     del T_cumul[0]

#     origins = [T[:3, 3] for T in T_cumul[:-1]]
#     z_axes = [T[:3, 2] for T in T_cumul[:-1]]
#     o_n = T_cumul[-1][:3, 3]

#     Jv = [np.cross(z_axes[i], o_n - origins[i]) for i in range(6)]
#     Jw = [z_axes[i] for i in range(6)]

#     J = np.vstack((np.array(Jv).T, np.array(Jw).T))
#     J[np.abs(J) < 0.0001] = 0
#     J = np.round(J, 2)
#     return J

# def check_singularity(J):
#     rank = np.linalg.matrix_rank(J)
#     cond_num = np.linalg.cond(J)

#     print(f"  Jacobian Rank: {rank}")
#     print(f"  Condition Number: {cond_num:.2f}")

#     if rank < 6:
#         print("  ❗ Singularity Detected: Jacobian is rank-deficient")
#     elif cond_num > 1000:
#         print("  ⚠️ Near-Singularity: Jacobian is ill-conditioned")
#     else:
#         print("  ✅ Jacobian is well-conditioned")

    # Final output
    for i, sol in enumerate(all_solutions):
        if not is_within_limits(sol):
            exit()

        is_valid, pos_err, rot_err = check_solution_error(sol, np.array([px, py, pz]), ROT_EE)

        if is_valid:
            angles_deg.append( np.degrees(sol))
            break

print(len(angles_deg))
print(angles_deg)


















# t = np.linspace(0, time, 100)
# plt.figure(figsize=(15, 12))

# plt.subplot(3, 1, 1)
# for i in range(6):
#     plt.plot(t, position_profile[i], label=f'Joint {i+1}')
# plt.title('Joint Positions')
# plt.ylabel('Position (rad)')
# plt.legend()

# plt.subplot(3, 1, 2)
# for i in range(6):
#     plt.plot(t, velocity_profile[i], label=f'Joint {i+1}')
# plt.title('Joint Velocities')
# plt.ylabel('Velocity (rad/s)')
# plt.legend()

# plt.subplot(3, 1, 3)
# for i in range(6):
#     plt.plot(t, acceleration_profile[i], label=f'Joint {i+1}')
# plt.title('Joint Accelerations')
# plt.ylabel('Acceleration (rad/s²)')
# plt.xlabel('Time (s)')
# plt.legend()

# plt.tight_layout()
# plt.show()