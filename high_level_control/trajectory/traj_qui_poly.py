import matplotlib.pyplot as plt
import numpy as np

max_velocity = 1500 #change the values 
max_acceleration = 4190  #change the values 
position_change = np.array([[0,2], [1,4], [0.2,1], [0.3,1.3], [0,1.9], [0.1,1.6]]) #change in theta of each joint 
time = 1 #time taken (can be changed by code)


def quintic_trajectory_coeffs(positions,time):
    coefficient = []
    coefficient_velo = []
    coefficient_acc = []

    for position in positions:
      theta_start_n = position[0]
      theta_end_n = position[1]
      start_velocity = 0
      end_velocity = 0
      start_acceleration = 0
      end_acceleration = 0

      start_time = 0
      end_time = time

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



def trajectory_generator(coefficient, coefficient_velo, coefficient_acc):
    global time , flag
    time_points = np.linspace(0, time, 100)
    
    position = []
    velocity = []
    velocity_max = []
    acceleration = []
    acceleration_max = []

    for j in range(0,6):

      position.append(np.polyval(coefficient[j], time_points))
      velocity.append( np.polyval(coefficient_velo[j], time_points))
      acceleration.append(np.polyval(coefficient_acc[j], time_points))
      velocity_max.append(np.max(velocity[j]))
      acceleration_max.append(np.max(acceleration[j]))
    
    if np.max(velocity_max) > max_velocity:
      time =time+0.01
      position.clear()
      velocity.clear()
      acceleration.clear()
      velocity_max.clear()
      acceleration_max.clear()

    elif np.max(acceleration_max) > max_acceleration:
      time =time+0.01
      position.clear()
      velocity.clear()
      acceleration.clear()
      velocity_max.clear()
      acceleration_max.clear()
    else:
       flag = False
       print ('max velocity', np.max(velocity_max))
       print ('max acceleration', np.max(acceleration_max))
       
  
    return position, velocity, acceleration


flag = True

while flag is True:
  coefficient, coefficient_velo, coefficient_acc = quintic_trajectory_coeffs(position_change, time)
  theta_pos, theta_vel, theta_acc = trajectory_generator(coefficient, coefficient_velo, coefficient_acc)


print('taken time is:',time )
print('position is:',theta_pos )
print('velocity is:',theta_vel )
print('acceleration is:',theta_acc )


t = np.linspace(0, time, 100)

plt.figure(figsize=(15, 12))

plt.subplot(3, 1, 1)
for i in range(6):
    plt.plot(t, theta_pos[i], label=f'Theta {i+1}')
plt.title('Joint Positions')
plt.ylabel('Position (rad)')
plt.legend()

plt.subplot(3, 1, 2)
for i in range(6):
    plt.plot(t, theta_vel[i], label=f'Theta {i+1}')
plt.title('Joint Velocities')
plt.ylabel('Velocity (rad/s)')
plt.legend()

plt.subplot(3, 1, 3)
for i in range(6):
    plt.plot(t, theta_acc[i], label=f'Theta {i+1}')
plt.title('Joint Accelerations')
plt.ylabel('Acceleration (rad/s²)')
plt.xlabel('Time (s)')
plt.legend()

plt.tight_layout()
plt.show()
