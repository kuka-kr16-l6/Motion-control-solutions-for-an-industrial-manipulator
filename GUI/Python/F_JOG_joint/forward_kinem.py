import numpy as np

# Define DH parameters (numerical values)
d1, d2, d3, d4, d5, d6, d7 = 0.675, 0, 0, 0.970, 0, 0, 0.115  # Link offsets
a1, a2, a3, a4, a5, a6, a7 = 0.26, 0.680, -0.035, 0, 0, 0, 0    # Link lengths
alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = -np.pi/2, 0, -np.pi/2, np.pi/2, -np.pi/2, 0  # Twist angles

# Standard DH Transformation Function (numerical)
def TF_Matrix(alpha, a, d, q):
    c_q, s_q = np.cos(q), np.sin(q)
    c_a, s_a = np.cos(alpha), np.sin(alpha)
    return np.array([
        [c_q, -s_q, 0, a],
        [s_q * c_a, c_q * c_a, -s_a, -s_a * d],
        [s_q * s_a, c_q * s_a, c_a, c_a * d],
        [0, 0, 0, 1]
    ])


# Compute transformation matrices for given joint angles
def compute_T0_EE(q_values):
    t1, t2, t3, t4, t5, t6 = q_values
    T0_1 = TF_Matrix(0, 0, d1, t1)
    T1_2 = TF_Matrix(-np.pi/2, a1, 0, t2 - np.pi/2)
    T2_3 = TF_Matrix(0, a2, 0, t3)
    T3_4 = TF_Matrix(-np.pi/2, a3, d4, t4)
    T4_5 = TF_Matrix(np.pi/2, 0, 0, t5)
    T5_6 = TF_Matrix(-np.pi/2, 0, 0, t6)
    T6_EE = TF_Matrix(0, 0, d7, 0)

    T0_EE = T0_1 @ T1_2 @ T2_3 @ T3_4 @ T4_5 @ T5_6 @ T6_EE
    return T0_EE
def F_K (theta):
    m_forward = compute_T0_EE(theta)
    # print ( m_forward)
    x = m_forward[0][3] 
    y = m_forward[1][3]
    z = m_forward[2][3]
    roll = np.rad2deg(np.arctan2(m_forward[2][1],m_forward[2][2]))
    pitch = np.rad2deg(np.arctan2(-m_forward[2][0],np.sqrt(m_forward[0][0]**2+m_forward[1][0]**2)))
    yaw = np.rad2deg(np.arctan2(m_forward[1][0],m_forward[0][0]))
    # print([x,y,z,roll,pitch,yaw])
    return [x*1000,y*1000,z*1000,roll,pitch,yaw]

# def main(theta):
#     F_K(theta)

# if __name__ == "__main__":
#     x = [np.deg2rad(45),np.deg2rad(40.3),np.deg2rad(20.5),np.deg2rad(16.78),np.deg2rad(1),0]
#     main(x)