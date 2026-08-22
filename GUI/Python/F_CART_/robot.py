import numpy as np

class robotRobot:
    def __init__(self):
        self.d1, self.d4, self.d7 = 0.675, 0.97, 0.115
        self.a1, self.a2, self.a3 = 0.26, 0.680, -0.035
        self.joint_limits = [
            (-np.pi, np.pi),
            (-1.1344, 2.18166),
            (-3.8397, 1.117),
            (-6.1086, 6.1086),
            (-2.268, 2.268),
            (-6.1086, 6.1086)
        ]

    def tf_matrix(self, alpha, a, d, q):
        c_q, s_q = np.cos(q), np.sin(q)
        c_a, s_a = np.cos(alpha), np.sin(alpha)
        return np.array([
            [c_q, -s_q, 0, a],
            [s_q * c_a, c_q * c_a, -s_a, -s_a * d],
            [s_q * s_a, c_q * s_a, c_a, c_a * d],
            [0, 0, 0, 1]
        ])