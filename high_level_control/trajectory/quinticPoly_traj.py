import matplotlib.pyplot as plt
import numpy as np

class trajectory:
    def __init__(self, current_theta, target_theta, max_acceleration, max_velocity,time_,time_steps_):
        self.initial_theta = np.array(current_theta)
        self.final_theta = np.array(target_theta)
        self.positions = list(zip(self.initial_theta, self.final_theta))
        self.max_acceleration_ = max_acceleration
        self.max_velocity_ = max_velocity
        self.time__ = time_
        self.time_steps = time_steps_
        self.flag = True

    def quintic_trajectory_coeffs(self ):
        coefficient = []
        coefficient_velo = []
        coefficient_acc = []

        for position in self.positions:
            theta_start_n = position[0]
            theta_end_n = position[1]
            start_velocity = 0
            end_velocity = 0
            start_acceleration = 0
            end_acceleration = 0

            start_time = 0
            end_time = self.time__

            equations = np.array([
                [1, start_time, start_time**2, start_time**3, start_time**4, start_time**5],
                [1, end_time, end_time**2, end_time**3, end_time**4, end_time**5],
                [0, 1, 2*start_time, 3*start_time**2, 4*start_time**3, 5*start_time**4],
                [0, 1, 2*end_time, 3*end_time**2, 4*end_time**3, 5*end_time**4],
                [0, 0, 2, 6*start_time, 12*start_time**2, 20*start_time**3],
                [0, 0, 2, 6*end_time, 12*end_time**2, 20*end_time**3]
                ])

            boundary_conditions = np.array([theta_start_n,theta_end_n, start_velocity, end_velocity, start_acceleration, end_acceleration])
            
            coeffs = np.linalg.solve(equations, boundary_conditions)
            velocity_coeffs = np.polyder(coeffs[::-1], 1)
            acceleration_coeffs = np.polyder(coeffs[::-1], 2) 

            coefficient.append(coeffs[::-1])
            coefficient_velo.append(velocity_coeffs)
            coefficient_acc.append(acceleration_coeffs)

        return coefficient, coefficient_velo, coefficient_acc


    def trajectory_generator(self, coeffs, coeffs_vel, coeffs_acc):
        time_points = np.linspace(0, self.time__, self.time_steps)
        pos, vel, acc = [], [], []
        max_vels, max_accs = [], []

        for j in range(len(coeffs)):
            pos_j = np.polyval(coeffs[j], time_points)
            vel_j = np.polyval(coeffs_vel[j], time_points)
            acc_j = np.polyval(coeffs_acc[j], time_points)

            pos.append(pos_j)
            vel.append(vel_j)
            acc.append(acc_j)
            max_vels.append(np.max(np.abs(vel_j)))
            max_accs.append(np.max(np.abs(acc_j)))

        return pos, vel, acc, max(max_vels), max(max_accs)

    def Quintic_trajectory(self):
        while True:
            coeffs, coeffs_vel, coeffs_acc = self.quintic_trajectory_coeffs()
            pos, vel, acc, max_vel, max_acc = self.trajectory_generator(coeffs, coeffs_vel, coeffs_acc)

            if max_vel > self.max_velocity_ or max_acc > self.max_acceleration_:
                self.time__ += 0.001  
            else:
                print('Final time:', self.time__)
                print('Max velocity reached:', max_vel)
                print('Max acceleration reached:', max_acc)
                return pos, vel, acc




def main ():
    current_theta = np.array([0,0,0,0,0,0])
    final_theta = np.array([1,1,1,1,1,1])
    time_ = 0.001
    max_velocity = 1500
    max_acceleration = 240000
    time_steps = 100
    traj= trajectory(current_theta, final_theta, max_acceleration, max_velocity,time_, time_steps)
    theta_pos, theta_vel, theta_acc = traj.Quintic_trajectory()

    
    print('position is:',theta_pos )
    print('velocity is:',theta_vel )
    print('acceleration is:',theta_acc )

if __name__ == "__main__":
    main()