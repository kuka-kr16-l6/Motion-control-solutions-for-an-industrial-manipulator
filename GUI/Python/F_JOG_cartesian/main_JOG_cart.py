import numpy as np 
from .inv_kinem import InverseKinematicsSolver
from .inverse_J import Jacobian
from .quintic_cart import trajectory
from .robot import robotRobot
from F_JOG_joint.forward_kinem import F_K
robot = robotRobot()

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

def trajectory_cart (current_pos, final_pos):
    start_velocity = 0
    end_velocity = 0
    start_acceleration = 0
    end_acceleration = 0
    max_velocity = 0.5
    max_acceleration = 1.25
    time_steps = 100
    traj= trajectory(current_pos, final_pos, start_velocity, end_velocity, start_acceleration, end_acceleration, max_acceleration, max_velocity, time_steps)
    pos, vel, acc, time__ = traj.Quintic_trajectory()
    return pos, vel, acc, time__, time_steps

def vel_kinematics(current_theta):
    Jacob= Jacobian(robot)
    J = Jacob.compute(current_theta)
    return J

def cart_calc(current_pos, current_theta, final_pos):
    pos, vel, acc, time__ , time_steps= trajectory_cart(current_pos, final_pos)
    # print("current_theta_inv_kinematics: ",np.rad2deg(current_theta))
    # print("used cart first point :", np.rad2deg(Inv_k_init(current_pos)))
    theta_p = [current_theta]
    vel_joint_p = [[0,0,0,0,0,0]]
    for i in range(1,len(pos[0])):
        px = pos[0][i]
        py = pos[1][i]
        pz = pos[2][i]
        roll = pos[3][i]
        pitch = pos[4][i]
        yaw = pos[5][i]
        vx = vel[0][i]
        vy = vel[1][i]
        vz = vel[2][i]
        vroll = vel[3][i]
        vpitch = vel[4][i]
        vyaw = vel[5][i]
        current_pos = [px,py,pz,roll,pitch,yaw]
        velocity = np.array([vx,vy,vz,vroll,vpitch,vyaw])
        theta = Inv_k(current_theta,current_pos)                  ## theta angles
        if theta is None:
            return None, None, 0, 0
        for i in range (3,6):
            if (theta[i] - current_theta[i]) > np.pi:
                theta[i]= theta[i] - (np.pi*2)
            elif (theta[i] - current_theta[i]) < -np.pi:
                theta[i]= theta[i] + (np.pi*2)
        
        j = vel_kinematics(theta)
        
        v_j = np.linalg.pinv(j)@ velocity.T                        ## speed joint speed
        current_theta = theta
        theta_p.append(np.rad2deg(theta))
        vel_joint_p.append(np.rad2deg(v_j.T))
    
    theta_p[0] = np.rad2deg(theta_p[0])
    vel_joint_p[0] = np.rad2deg(vel_joint_p[0])
    
    theta_p = np.array(theta_p)
    vel_joint_p = np.array(vel_joint_p)*125/6

    # print("theta_p: ", theta_p)
    # print("vel_joint_p: ", vel_joint_p)

    return theta_p, vel_joint_p, time__, time_steps


# def main ( ):
#     current_pos = [1.2862298967702825,0.39323994285208097,1.39,np.deg2rad(-135),np.deg2rad(-90),np.deg2rad(-27.999999996)]
    
#     t = Inv_k_init(current_pos)
#     print (np.rad2deg(t))

# if __name__ == "__main__":
#     main()