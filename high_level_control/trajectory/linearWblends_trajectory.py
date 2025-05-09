import numpy as np 
import matplotlib.pyplot as plt

class trajectory:

    def __init__(self, current_theta, target_theta, max_acceleration, max_velocity,alpha_):
        self.initial_theta = np.array(current_theta)
        self.final_theta = np.array(target_theta)
        self.delta_theta = list(zip(self.initial_theta, self.final_theta))
        self.max_acceleration_ = max_acceleration
        self.max_velocity_ = max_velocity
        self.alpha = alpha_
            
    def time_calc(self, delta_theta , max_acceleration_, max_velocity_, alpha):
        max_time=[]
        for joint in delta_theta:
            delta = np.abs(joint[1]-joint[0])
            time_acc = np.sqrt((delta) /(max_acceleration_*alpha*(1-alpha)))
            time_velo = delta / (max_velocity_ * (1 - alpha))
            max_time.append(max(time_acc,time_velo))
        
        print("time is :", max(max_time))
        return max(max_time)


    def linear_blends_generator(self, delta_theta , time_ , alpha):

        timesteps = np.linspace(0,time_,100)
        ta = time_ * alpha
        tb = time_ - (ta)
        position_profile = []
        velocity_profile = []
        acceleration_profile = []

        for joint in delta_theta:
            start_theta = joint[0]
            end_theta = joint[1]
            parabola_acceleration = (end_theta - start_theta) / (ta * (time_ - ta))
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
                    position.append(end_theta - (parabola_acceleration*0.5*(time_ -timestep)**2  ))
                    velocity.append(parabola_acceleration*(time_-timestep))
                    acceleration.append(-parabola_acceleration)

            position_profile.append(position)
            velocity_profile.append(velocity)
            acceleration_profile.append(acceleration)

        return position_profile, velocity_profile, acceleration_profile
    
    def trajectory_generator(self):
        time_ = self.time_calc(self.delta_theta, self.max_acceleration_, self.max_velocity_, 0.3)
        position_profile, velocity_profile, acceleration_profile = self.linear_blends_generator(self.delta_theta, time_, 0.3)
        print('max time is', time_)
        return position_profile, velocity_profile

def main():
    current_theta = np.array([0,0,0,0,0,0])
    final_theta = np.array([1,1,1,1,1,1])
    alpha = 0.3
    max_velocity = 1500
    max_accleration = 240000
    traj = trajectory(current_theta,final_theta, max_accleration, max_velocity, alpha)
    position_p, velocity_p = traj.trajectory_generator()

    print('position profile:', position_p)
    print('veloity profile:', velocity_p)
    

if __name__ == '__main__':
    main()