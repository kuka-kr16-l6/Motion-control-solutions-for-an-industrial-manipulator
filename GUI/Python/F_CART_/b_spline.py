import numpy as np
import math
from .rmf_orientation import compute_rmf
###########
# position =[[x1,x2,....,xn],[y1,y2,....,yn],[z1,z2,....,zn]]
###########

def compute_knot_vector(position,degree):
    #cord length distribution 
    px = position[0]
    py = position[1]
    pz = position[2]
    acc = 0
    dis = []
    knots=[0]
    knot_vector = [0]*(degree+1) 
    for k in range(1,len(px)):
        distance = np.sqrt((px[k]-px[k-1])**2+(py[k]-py[k-1])**2+(pz[k]-pz[k-1])**2)
        dis.append(distance)
        acc = acc + distance 
    for i in range(1, len(px)):
        u = sum(dis[:i]) / acc
        knots.append(u)
    for i in range(0,len(knots)-1):
        knot_vector.append( (knots[i]+knots[i+1])/2)
    knot_vector += [1]*(degree+1) 
    return knot_vector, knots

def span(independent_variable, knot_vector , degree):
    n_knot = len(knot_vector)-1
    high = n_knot - degree
    low = degree
    if independent_variable == knot_vector[high]:
        mid = high 
    else:
        mid = int((high+low)/2)
        while independent_variable < knot_vector[mid] or independent_variable >=knot_vector[mid+1]:
            if independent_variable == knot_vector[mid+1]:
                mid = mid+1
            else:
                if(independent_variable > knot_vector[mid]):
                    low = mid
                else:
                    high = mid 
                mid = int((high+low)/2)
    return mid 

def Basis_function ( independent_variable, degree, knot_vector):
    DL = [0]*(degree+1)
    DR = [0]*(degree+1)
    B = [0]*(degree+1)
    B[0]=1
    span_knot = span(independent_variable,knot_vector,degree)
    for j in range(1, degree+1):
        DL[j] = independent_variable -knot_vector[span_knot+1-j]
        DR[j] = knot_vector[span_knot+j] - independent_variable
        acc = 0
        for r in range(0,j):
            temp =  B[r]/(DR[r+1]+DL[j-r])
            B[r] = acc + DR[r+1] *temp
            acc = DL[j-r] *temp
        B[j]=acc
    B = B_square(B, independent_variable, span_knot,knot_vector,degree)
    return B

def ders_basis_funs(span_knot, independent_variable, degree, knot_vector):
    der_no = degree
    DL = np.zeros(degree+1)
    DR = np.zeros(degree+1)
    Du = np.zeros((degree+1, degree+1))
    ders = np.zeros((der_no+1, degree+1))
    a = np.zeros((2, degree+1))
    Du[0][0] = 1.0
    for j in range(1, degree+1):
        DL[j] = independent_variable - knot_vector[span_knot+1-j]
        DR[j] = knot_vector[span_knot+j] - independent_variable
        acc = 0.0
        for r in range(0, j):
            Du[j][r] = DR[r+1] + DL[j-r]
            temp = Du[r][j-1] / Du[j][r]
            Du[r][j] = acc + DR[r+1] * temp
            acc = DL[j-r] * temp
        Du[j][j] = acc
    for j in range(degree+1):
        ders[0][j] = Du[j][degree]
    for r in range(0, degree+1):
        s1 = 0
        s2 = 1
        a[0][0] = 1.0
        for k in range(1, der_no+1):
            d = 0.0
            rk = r - k
            pk = degree - k
            if r >= k:
                a[s2][0] = a[s1][0] / Du[pk+1][rk]
                d = a[s2][0] * Du[rk][pk]
            if rk >= -1:
                j1 = 1
            else:
                j1 = -rk
            if r - 1 <= pk:
                j2 = k - 1
            else:
                j2 = degree - r
            for j in range(j1, j2+1):
                a[s2][j] = (a[s1][j] - a[s1][j-1]) / Du[pk+1][rk+j]
                d += a[s2][j] * Du[rk+j][pk]
            if r <= pk:
                a[s2][k] = -a[s1][k-1] / Du[pk+1][r]
                d += a[s2][k] * Du[r][pk]
            ders[k][r] = d
            s1, s2 = s2, s1
    rfact = degree
    for k in range(1, der_no+1):
        for j in range(degree+1):
            ders[k][j] *= rfact
        rfact *= (degree - k)
    pos_basis = B_square(ders[0],independent_variable, knot_vector,degree)
    vel_basis = B_square(ders[1],independent_variable, knot_vector,degree)
    acc_basis = B_square(ders[2],independent_variable, knot_vector,degree)
    jerk_basis = B_square(ders[3],independent_variable, knot_vector,degree)
    snap_basis = B_square(ders[4],independent_variable, knot_vector,degree)
    return pos_basis, vel_basis, acc_basis, jerk_basis, snap_basis

def B_square(B, independent_variable, knot_vector, degree):
    B = list(B)
    span_knot = span(independent_variable,knot_vector,degree)
    B = [x for x in B if x != 0]
    nonzero = len(B)
    target = len(knot_vector) - degree-1
    if span_knot == degree:
        for _ in range(nonzero, target):
            B.append(0)
    elif independent_variable == 1 :

        for _ in range(nonzero, target):
            B.insert(0, 0)
    else:
        for _ in range(span_knot-degree):
            B.insert(0, 0)
        while len(B) < target:
            B.append(0)
    return B
    
def compute_control_points (position, degree, knot_vector, knots):
    #boundary conditions 
    B=[]
    acceleration_init = [0,0, 0]
    speed_init = [0, 0, 0]
    acceleration_final = [0,0,0]
    speed_final = [0 ,0, 0]
    for i in range(degree, len(knots)+degree):
        pos_basis, vel_basis , acc_basis, jerk_basis , snap_basis = ders_basis_funs(i,knots[i-degree],degree,knot_vector)
        if i== degree:
            B.append(pos_basis)
            B.append(vel_basis)
            B.append(acc_basis)
        elif i==len(knots)+degree-1:
            B.append(acc_basis)
            B.append(vel_basis)
            B.append(pos_basis)
        else: 
            B.append(pos_basis)
    points = list(zip(position[0], position[1], position[2]))
    points.insert(1,acceleration_init)
    points.insert(1,speed_init)
    points.insert(len(points)-1,acceleration_final) 
    points.insert(len(points)-1,speed_final)
    b = np.linalg.inv(B)
    control_points = b@points
    control_points =  np.transpose(control_points)
    return control_points

# def compute_control_points (position, degree, knot_vector, knots):
#     #cyclic condition
#     B=[]
#     acceleration_init = [0,0, 0]
#     speed_init = [0, 0, 0]
#     acceleration_final = [0,300,0]
#     speed_final = [-20 ,0, 0]
#     for i in range(degree, len(knots)+degree):
#         pos_basis, vel_basis , acc_basis, jerk_basis , snap_basis = ders_basis_funs(i,knots[i-degree],degree,knot_vector)
#         B.append(pos_basis)
#         if i== degree:
#             velo_init = np.array(vel_basis)
#             acc_init = np.array(acc_basis)
#             jerk_init = np.array(jerk_basis)
#             snap_init = np.array(snap_basis)
#         elif i==len(knots)+degree-1:
#             velo_final = np.array(vel_basis)
#             acc_final = np.array(acc_basis)
#             jerk_final = np.array(jerk_basis)
#             snap_final = np.array(snap_basis)
#     B.append(velo_init-velo_final)
#     B.append(acc_init-acc_final)    
#     B.append(jerk_init-jerk_final)
#     B.append(snap_init-snap_final)        
#     points = list(zip(position[0], position[1], position[2]))
#     points.append([0,0,0])
#     points.append([0,0,0])
#     points.append([0,0,0]) 
#     points.append([0,0,0])
#     b = np.linalg.inv(B)
#     control_points = b@points
#     control_points =  np.transpose(control_points)
#     return control_points

def Bsplinepoint(independent_variable , knot_vector, degree, control_p , d):
    i = span(independent_variable, knot_vector, degree)
    b = ders_basis_funs (i, independent_variable, degree, knot_vector)    

    position_p = [0]*d
    velo_p = [0]*d
    acc_p = [0]*d
    jerk_p = [0]*d
    snap_p = [0]*d
    max_vel = 0
    max_acc = 0
    for k in range(0,d):
        for j in range(0, len(b[0])):
            position_p[k] = position_p[k] + (control_p[k][j]*b[0][j])
            velo_p[k] = velo_p[k] + (control_p[k][j]*b[1][j])
            max_vel = max(max_vel, abs(velo_p[k]))  
            acc_p[k] = acc_p[k] + (control_p[k][j]*b[2][j])
            max_acc = max(max_acc, abs(acc_p[k]))
            jerk_p[k] = jerk_p[k] + (control_p[k][j]*b[3][j])
            snap_p[k] = snap_p[k] + (control_p[k][j]*b[4][j])
    return position_p, velo_p, acc_p, jerk_p, snap_p, max_vel, max_acc

def generate_path(positions):
    degree = 4
    dimension = 3
    # print ("posiitions ",positions )
    # positions = [[3.31,-3.01,-1.07,4.48,1.52,3,-2,-1,2],[-2.38,3.53,5.81,2.97,-1.25,3,4,-1,0],[1,2,3,4,5,6,7,8,9]]
    knot_vector, knots = compute_knot_vector(positions,degree)
    time_steps=[]
    time_steps_perseg = 50
    for i in range(len(knots)-1):
        times = np.linspace(knots[i], knots[i+1], time_steps_perseg)
        time_steps.extend(times)
        time_steps = time_steps[:-1]
    control_points =  compute_control_points(positions,degree,knot_vector, knots)
    position_p=[]
    velo_p = []
    acc_p =[]
    jerk_p =[]
    snap_p =[]
    prev_roll = np.deg2rad(-135)
    prev_pitch = np.deg2rad(-45)
    prev_yaw = np.deg2rad(-90)
    max_vel = 0
    max_acc = 0

    for i in range(1, len(time_steps)):
        if time_steps[i]==1:
            time_steps[i] = time_steps[i] - 1e-16
        position , velocity, acceleration, jerk, snap, max_vel_p, max_acc_p= Bsplinepoint(time_steps[i], knot_vector,degree,control_points,dimension)
        max_vel = max(max_vel, max_vel_p)
        max_acc = max(max_acc, max_acc_p)
        position_p.append(position )
        velo_p.append(velocity)
        acc_p.append(acceleration)
        jerk_p.append(jerk)
        snap_p.append(snap)
    np.set_printoptions(threshold=np.inf)
    position_p = np.array(position_p)
    velo_p = np.array(velo_p)
    time_steps = np.array(time_steps[1:])
    orientations, ang_velocities, ang_accs, frames = compute_rmf(
        position_p, timesteps=time_steps
    )
    # print("pos", position_p)
    # orientations:   (n, 3) degrees  — roll, pitch, yaw
    # ang_velocities: (n, 3) deg/s
    # ang_accs:       (n, 3) deg/s²

    # update max vel/acc with angular contributions
    max_vel = max(max_vel, float(np.max(np.abs(ang_velocities))))
    max_acc = max(max_acc, float(np.max(np.abs(ang_accs))))

    # combine position + orientation into 6DOF profile
    p_p = np.hstack([position_p, orientations])    # (n, 6)
    v_p = np.hstack([velo_p,     ang_velocities])
    # print ('positions_Or',p_p)
    return p_p, v_p, time_steps, max_vel, max_acc 

      
# def plot_control_points(points, c_points, show_lines=True):
#     points = np.array(points)
#     X = points[:,0]
#     Y = points[:,1]
#     Z = points[:,2]

#     c_points = np.array(c_points)
#     x = c_points[0,:]
#     y = c_points[1,:]
#     z = c_points[2,:]
#     fig = plt.figure()

#     ax = fig.add_subplot(111, projection='3d')
#     ax.scatter(X, Y, Z, s=3)
#     ax.scatter(x, y, z, s=5)
    # if show_lines:
    #     ax.plot(x, y, z, color='blue')
    # for i in range(len(points)):
    #     x, y, z , roll, pitch , yaw  = points[i]
    #     R_x = np.array([[1,0,0],
    #             [0,np.cos(roll),-np.sin(roll)],
    #             [0,np.sin(roll),np.cos(roll)]])  
    #     R_y = np.array([[np.cos(pitch),0,np.sin(pitch)],
    #             [0,1,0],
    #             [-np.sin(pitch),0,np.cos(pitch)]]) 
    #     R_z = np.array([[np.cos(yaw),-np.sin(yaw),0],
    #             [np.sin(yaw),np.cos(yaw),0],
    #             [0  ,0,1]]) 
    #     R = R_x @ R_y @ R_z  
    #     # Columns of R are local axes
    #     ax.quiver(x, y, z, R[0,0], R[1,0], R[2,0], length=0.5, color='r')  
    #     ax.quiver(x, y, z, R[0,1], R[1,1], R[2,1], length=0.5, color='g')  
    #     ax.quiver(x, y, z, R[0,2], R[1,2], R[2,2], length=0.5, color='k')  
    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")
    # ax.set_title("3D Control Points")
    # plt.show()

# def sub_plotting (points,time_steps):
#     points = np.array(points)    
#     x = points[:, 0]
#     y = points[:, 1]
#     z = points[:, 2]


#     fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

#     axs[0].plot(time_steps[1:], x)
#     axs[0].set_title("Velocity in X-axis")
#     axs[0].set_ylabel("Vx")

#     axs[1].plot(time_steps[1:], y)
#     axs[1].set_title("Velocity in Y-axis")
#     axs[1].set_ylabel("Vy")

#     axs[2].plot(time_steps[1:], z)
#     axs[2].set_title("Velocity in Z-axis")
#     axs[2].set_ylabel("Vz")
#     axs[2].set_xlabel("Time index")


#     plt.tight_layout()
#     plt.show()

# def sub_plotting_acc (points,time_steps):
#     points = np.array(points)    
#     x = points[:, 0]
#     y = points[:, 1]
#     z = points[:, 2]


#     fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

#     axs[0].plot(time_steps[1:], x)
#     axs[0].set_title("Acc in X-axis")
#     axs[0].set_ylabel("Ax")

#     axs[1].plot(time_steps[1:], y)
#     axs[1].set_title("Acc in Y-axis")
#     axs[1].set_ylabel("Ay")

#     axs[2].plot(time_steps[1:], z)
#     axs[2].set_title("Acc in Z-axis")
#     axs[2].set_ylabel("Az")
#     axs[2].set_xlabel("Time index")


#     plt.tight_layout()
#     plt.show()

# def sub_plotting_jerk (points,time_steps):
#     points = np.array(points)    
#     x = points[:, 0]
#     y = points[:, 1]
#     z = points[:, 2]


#     fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

#     axs[0].plot(time_steps[1:], x)
#     axs[0].set_title("Jerk in X-axis")
#     axs[0].set_ylabel("Jx")

#     axs[1].plot(time_steps[1:], y)
#     axs[1].set_title("Jerk in Y-axis")
#     axs[1].set_ylabel("Jy")

#     axs[2].plot(time_steps[1:], z)
#     axs[2].set_title("Jerk in Z-axis")
#     axs[2].set_ylabel("Jz")
#     axs[2].set_xlabel("Time index")


#     plt.tight_layout()
#     plt.show()

# def sub_plotting_snap (points,time_steps):
#     points = np.array(points)    
#     x = points[:, 0]
#     y = points[:, 1]
#     z = points[:, 2]


#     fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

#     axs[0].plot(time_steps[1:], x)
#     axs[0].set_title("snap in X-axis")
#     axs[0].set_ylabel("Sx")

#     axs[1].plot(time_steps[1:], y)
#     axs[1].set_title("snap in Y-axis")
#     axs[1].set_ylabel("Sy")

#     axs[2].plot(time_steps[1:], z)
#     axs[2].set_title("snap in Z-axis")
#     axs[2].set_ylabel("Sz")
#     axs[2].set_xlabel("Time index")


#     plt.tight_layout()
#     plt.show()

# if __name__ == "__main__":
#     generate_path()
