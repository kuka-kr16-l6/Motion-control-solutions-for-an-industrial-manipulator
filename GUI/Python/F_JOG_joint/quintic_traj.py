import numpy as np

class trajectory:
    def __init__(self, current_theta, target_theta, start_velocity, end_velocity, start_acceleration, end_acceleration, max_acceleration, max_velocity,time_steps_):
        self.gearreductionj123 = 125
        self.gearreductionj4 = 670/9
        self.gearreductionj5 = 380/9
        self.gearreductionj6 = 410/17
        self.initial_theta = np.array(current_theta)
        self.final_theta = np.array(target_theta)
        self.positions = list(zip(self.initial_theta, self.final_theta))
        self.start_velocity_ = start_velocity
        self.end_velocity_ = end_velocity
        self.start_acceleration_ = start_acceleration
        self.end_acceleration_ = end_acceleration
        # acc in deg/s^2
        self.max_acceleration_j123 = (max_acceleration * (360/60**2))/ self.gearreductionj123
        self.max_acceleration_j4 = (max_acceleration * (360/60**2))/ self.gearreductionj4
        self.max_acceleration_j5 = (max_acceleration * (360/60**2))/ self.gearreductionj5
        self.max_acceleration_j6 = (max_acceleration * (360/60**2))/ self.gearreductionj6
        # vel in deg/s
        self.max_velocity_j123 = (max_velocity *6)/ self.gearreductionj123
        self.max_velocity_j4 = (max_velocity *6)/ self.gearreductionj4
        self.max_velocity_j5 = (max_velocity *6)/ self.gearreductionj5
        self.max_velocity_j6 = (max_velocity *6)/ self.gearreductionj6
        self.time_steps = time_steps_
        self.flag = True

    def compute_time(self):

        h = 0
        theta_start = 0
        theta_end = 0
        idx = 0

        for i, position in enumerate(self.positions[:3]):
            dis = np.abs(position[1] - position[0])
            if dis > h:
                theta_start = position[0]
                theta_end = position[1]
                idx = i
            h = max(dis, h)

        # cases to check: (theta_start, theta_end, max_velocity, max_acceleration)
        cases = [
            (theta_start, theta_end, self.max_velocity_j123, self.max_acceleration_j123),
        ]

        last_three_limits = [
            (self.max_velocity_j4, self.max_acceleration_j4),
            (self.max_velocity_j5, self.max_acceleration_j5),
            (self.max_velocity_j6, self.max_acceleration_j6),
        ]

        for j, position in enumerate(self.positions[3:]):
            max_vel_j, max_acc_j = last_three_limits[j]
            cases.append((position[0], position[1], max_vel_j, max_acc_j))

        max_time = 0

        for theta_start_, theta_end_, max_velocity_, max_acceleration_ in cases:

            if abs(theta_end_ - theta_start_) < 1e-9:
                continue  # no displacement in this case, nothing to constrain

            start_time = 0
            end_time = 1

            equations = np.array([
                [1, start_time, start_time**2, start_time**3, start_time**4, start_time**5],
                [1, end_time, end_time**2, end_time**3, end_time**4, end_time**5],
                [0, 1, 2*start_time, 3*start_time**2, 4*start_time**3, 5*start_time**4],
                [0, 1, 2*end_time, 3*end_time**2, 4*end_time**3, 5*end_time**4],
                [0, 0, 2, 6*start_time, 12*start_time**2, 20*start_time**3],
                [0, 0, 2, 6*end_time, 12*end_time**2, 20*end_time**3]
            ])

            boundary_conditions = np.array([
                theta_start_, theta_end_,
                self.start_velocity_, self.end_velocity_,
                self.start_acceleration_, self.end_acceleration_
            ])

            coeffs = np.linalg.solve(equations, boundary_conditions)

            velocity_coeffs = np.polyder(coeffs[::-1], 1)
            acceleration_coeffs = np.polyder(coeffs[::-1], 2)
            jerk_coeffs = np.polyder(coeffs[::-1], 3)

            roots_velo = np.roots(acceleration_coeffs)
            roots_acc = np.roots(jerk_coeffs)

            M_1 = max(np.polyval(velocity_coeffs, roots_velo))
            M_2 = max(np.polyval(acceleration_coeffs, roots_acc))

            time_constrained_V = M_1 / max_velocity_
            time_constrained_a = np.sqrt(M_2 / max_acceleration_)

            joint_time = max(time_constrained_V, time_constrained_a)
            max_time = max(max_time, joint_time)
        return max_time
    
    def quintic_trajectory_coeffs(self , time__):
        coefficient = []
        coefficient_velo = []
        coefficient_acc = []

        for position in self.positions:
            theta_start_n = position[0]
            theta_end_n = position[1]


            start_time = 0
            end_time = time__

            equations = np.array([
                [1, start_time, start_time**2, start_time**3, start_time**4, start_time**5],
                [1, end_time, end_time**2, end_time**3, end_time**4, end_time**5],
                [0, 1, 2*start_time, 3*start_time**2, 4*start_time**3, 5*start_time**4],
                [0, 1, 2*end_time, 3*end_time**2, 4*end_time**3, 5*end_time**4],
                [0, 0, 2, 6*start_time, 12*start_time**2, 20*start_time**3],
                [0, 0, 2, 6*end_time, 12*end_time**2, 20*end_time**3]
                ])

            boundary_conditions = np.array([theta_start_n,theta_end_n, self.start_velocity_, self.end_velocity_, self.start_acceleration_, self.end_acceleration_])
            
            coeffs = np.linalg.solve(equations, boundary_conditions)
            velocity_coeffs = np.polyder(coeffs[::-1], 1)
            acceleration_coeffs = np.polyder(coeffs[::-1], 2) 

            coefficient.append(coeffs[::-1])
            coefficient_velo.append(velocity_coeffs)
            coefficient_acc.append(acceleration_coeffs)

        return coefficient, coefficient_velo, coefficient_acc

        
    def trajectory_generator(self, coeffs, coeffs_vel, coeffs_acc, time__):
        time_points = np.linspace(0, time__, self.time_steps)
        pos, vel, acc = [], [], []
        max_vels, max_accs = [], []

        gear_ratios = [
            self.gearreductionj123, self.gearreductionj123, self.gearreductionj123,
            self.gearreductionj4, self.gearreductionj5, self.gearreductionj6
        ]

        for j in range(len(coeffs)):
            pos_j = np.polyval(coeffs[j], time_points)
            vel_j = np.polyval(coeffs_vel[j], time_points)
            acc_j = np.polyval(coeffs_acc[j], time_points)

            gear_ratio = gear_ratios[j]

            # joint-side deg/s -> motor-side deg/s -> rpm
            vel_j_rpm = (vel_j * gear_ratio) / 6

            # joint-side deg/s^2 -> motor-side deg/s^2 -> sec^-2
            acc_j_motor = (acc_j * gear_ratio) / (360 / 60**2)

            pos.append(pos_j)
            vel.append(vel_j_rpm)
            acc.append(acc_j_motor)
            max_vels.append(np.max(np.abs(vel_j_rpm)))
            max_accs.append(np.max(np.abs(acc_j_motor)))

        return pos, vel, acc, max(max_vels), max(max_accs)

    def Quintic_trajectory(self):
        time__ = self.compute_time()
        coeffs, coeffs_vel, coeffs_acc = self.quintic_trajectory_coeffs(time__)
        pos, vel, acc, max_vel, max_acc = self.trajectory_generator(coeffs, coeffs_vel, coeffs_acc, time__)
        return pos, vel, acc

# def main():
#     current_theta = [0,0,0,0,0,0]
#     final_theta = [80,20,20,30,40,50]
#     start_velocity = 0
#     end_velocity = 0
#     start_acceleration = 0
#     end_acceleration = 0
#     max_velocity = 500
#     max_acceleration = 340000/(3*3)
#     time_steps = 100
#     traj = trajectory(current_theta, final_theta, start_velocity, end_velocity,
#                     start_acceleration, end_acceleration, max_acceleration, max_velocity, time_steps)
#     theta_pos, theta_vel, theta_acc = traj.Quintic_trajectory()
#     print("position", theta_pos)
#     print("position", theta_vel)


# if __name__ == "__main__":
#     main()
