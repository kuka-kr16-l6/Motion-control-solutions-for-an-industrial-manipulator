import numpy as np

class Jacobian:
    def __init__(self, robot):
        self.robot = robot

    def compute(self, thetas):
        r = self.robot
        dh_params = [
            (0, 0, r.d1, thetas[0]),
            (-np.pi/2, r.a1, 0, thetas[1] - np.pi/2),
            (0, r.a2, 0, thetas[2]),
            (-np.pi/2, r.a3, r.d4, thetas[3]),
            (np.pi/2, 0, 0, thetas[4]),
            (-np.pi/2, 0, 0, thetas[5]),
            (0, 0, r.d7, 0)
        ]

        T_cumul = [np.eye(4)]
        for alpha, a, d, q in dh_params:
            T_cumul.append(T_cumul[-1] @ r.tf_matrix(alpha, a, d, q))
        T_cumul = T_cumul[1:]

        origins = [T[:3, 3] for T in T_cumul[:-1]]
        z_axes = [T[:3, 2] for T in T_cumul[:-1]]
        o_n = T_cumul[-1][:3, 3]

        Jv = [np.cross(z_axes[i], o_n - origins[i]) for i in range(6)]
        Jw = [z_axes[i] for i in range(6)]
        J = np.vstack((np.array(Jv).T, np.array(Jw).T))
        return J

    def check_singularity(self, J):
        rank = np.linalg.matrix_rank(J)
        cond_num = np.linalg.cond(J)
        if rank < 6:
            return "❗ Singularity Detected: Jacobian is rank-deficient"
        elif cond_num > 1000:
            return "⚠️ Near-Singularity: Jacobian is ill-conditioned"
        else:
            return "✅ Jacobian is well-conditioned"