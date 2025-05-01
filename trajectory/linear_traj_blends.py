import numpy as np 
import matplotlib.pyplot as plt


position_change = np.array([[2,1],[2,1],[2,4],[3,1],[5,1],[2,3]])
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

t = np.linspace(0, time, 100)
plt.figure(figsize=(15, 12))

plt.subplot(3, 1, 1)
for i in range(6):
    plt.plot(t, position_profile[i], label=f'Joint {i+1}')
plt.title('Joint Positions')
plt.ylabel('Position (rad)')
plt.legend()

plt.subplot(3, 1, 2)
for i in range(6):
    plt.plot(t, velocity_profile[i], label=f'Joint {i+1}')
plt.title('Joint Velocities')
plt.ylabel('Velocity (rad/s)')
plt.legend()

plt.subplot(3, 1, 3)
for i in range(6):
    plt.plot(t, acceleration_profile[i], label=f'Joint {i+1}')
plt.title('Joint Accelerations')
plt.ylabel('Acceleration (rad/s²)')
plt.xlabel('Time (s)')
plt.legend()

plt.tight_layout()
plt.show()
