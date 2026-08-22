from .inv_kinem import InverseKinematicsSolver
from .inverse_J import Jacobian
from .robot import robotRobot
from .b_spline import generate_path
import numpy as np 

robot = robotRobot()
max_velocity = 1
max_acceleration = 2.5


def _b_spline (p):
    positions = p.T
    # print ("positions: ", positions)
    position_p, velocity_p, time_steps, max_vel, max_acc = generate_path(positions)
    # print ("_vel: ", velocity_p)
    # print ("time_steps: ", time_steps)
    v_scale = max_vel/max_velocity
    a_scale = np.sqrt(max_acc/max_acceleration)
    # time_steps = np.linspace(0,1/max(v_scale,a_scale),len(position_p))
    print ("time: ", min(v_scale,a_scale))
    # print ("max_vel: ", max_vel/maxvelocity_p(v_scale,a_scale), "max_acc: ", max_acc/max(v_scale,a_scale)**2)
    # print ("v_scale: ", v_scale, "a_scale: ", a_scale)
    velocity_p = velocity_p/max(v_scale,a_scale)
    return position_p, velocity_p, np.array(time_steps)*min(v_scale,a_scale)

def Inv_k_init( current_pos ):
    px,py,pz,roll,pitch, yaw = current_pos
    IK  = InverseKinematicsSolver(robot, px,py,pz,roll,pitch,yaw)
    current_theta = IK.get_best_solution()
    return current_theta

def Inv_k(previous_theta , current_pos ):
    px,py,pz,roll,pitch, yaw = current_pos
    IK  = InverseKinematicsSolver(robot, px,py,pz,roll,pitch,yaw, previous_theta)
    current_theta = IK.get_best_solution()
    return current_theta

def vel_kinematics(current_theta):
    Jacob= Jacobian(robot)
    J = Jacob.compute(current_theta)
    return J

def Bcart_calc(positions):
    pos, vel, time_steps = _b_spline(positions)
    # print ("pos",pos)
    # print ("pos: ", pos)
    # print ("vel: ", vel)
    current_theta = Inv_k_init(pos[0])
    # print ("current_theta: ", current_theta)
    theta_p = [current_theta]
    vel_joint_p = [[0,0,0,0,0,0]]
    for i in range(1,len(pos)):
        px = pos[i][0]
        py = pos[i][1]
        pz = pos[i][2]
        roll = pos[i][3]
        pitch = pos[i][4]
        yaw = pos[i][5]
        vx = vel[i][0]
        vy = vel[i][1]
        vz = vel[i][2]
        vroll = vel[i][3]
        vpitch = vel[i][4]
        vyaw = vel[i][5]
        current_pos = [px,py,pz,roll,pitch,yaw]
        velocity = np.array([vx,vy,vz,vroll,vpitch,vyaw])
        theta = Inv_k(current_theta,current_pos)                  ## theta angles
        # print ("theta: ", theta)     
        j = vel_kinematics(theta)
        
        v_j = np.linalg.pinv(j)@ velocity.T                        ## speed joint speed
        current_theta = theta
        theta_p.append(np.rad2deg(theta))
        vel_joint_p.append(np.rad2deg(v_j.T))
    
    theta_p[0] = np.rad2deg(theta_p[0])
    vel_joint_p[0] = np.rad2deg(vel_joint_p[0])
    
    theta_p = np.array(theta_p)
    vel_joint_p = np.array(vel_joint_p)
    vel_joint_p[:, 0:3] *= 125 / 6   
    vel_joint_p[:, 3]   *= 670 / 54  
    vel_joint_p[:, 4]   *= 380 / 54  
    vel_joint_p[:, 5]   *= 410 / 102 
    # print("theta_p: ", theta_p)
    # print("vel_joint_p: ", vel_joint_p)
    return theta_p, vel_joint_p, time_steps


# def main_cart():
#     positions = np.array([[1, 1, 1],
#                           [1, -0.4, 1],
#                           [1, 1, 1],])
#     theta_p, vel_joint_p, time_steps = Bcart_calc(positions)
    # print("theta_p: ", theta_p)
    # print("vel_joint_p: ", vel_joint_p)
    


# if __name__ == "__main__":
#     main_cart()