import numpy as np
import math


class tree:
    def __init__(self, n):
        self.x = n[0] 
        self.y = n[1]
        self.z = n[2]
        self.parent = None 

class rrt:
    def __init__(self, start, target, step, sample_goal_rate, iterations):
        self.P_start = tree(start)
        self.P_tartget = tree(target)
        self.step = step
        self.max_iteration =  iterations
        self.sample_goal_rate = sample_goal_rate
        self.vertex = [self.P_start]

    def pathplanning(self):
        for i in range(self.max_iteration):
            random_node = self.create_Random(self.sample_goal_rate)
            near_node = self.nearest_node(self.vertex, random_node)
            new_node = self.create_new_node(random_node, near_node)
            if new_node:
                self.vertex.append(new_node)
                dist, theta, phi = self.calc_dist_theta_phi(self.P_tartget,new_node)
                if dist <= self.step :
                    goal_node = self.create_new_node(self.P_tartget, new_node)
                    goal_node.parent = new_node
                    self.vertex.append(goal_node)
                    return self.compute_path(goal_node)
                
    def create_Random(self, sample_goal_rate):
        if np.random.random() > sample_goal_rate:
            return tree((np.random.uniform(0,10), np.random.uniform(0,10), np.random.uniform(0,10)))
        else:
            return self.P_start

    def nearest_node(self, treelist , rn):
        return treelist[int(np.argmin([np.sqrt((tr.x - rn.x)**2+(tr.y - rn.y)**2+(tr.z - rn.z)**2) for tr in treelist]))]

    def create_new_node(self, random_node, near_node):
        dist , theta, phi= self.calc_dist_theta_phi(random_node, near_node)
        step_size = min(dist,self.step )
        new_x = near_node.x + step_size*np.cos(theta)*np.cos(phi)
        new_y = near_node.y + step_size*np.sin(theta)*np.cos(phi)
        new_z = near_node.z + step_size*np.sin(phi)
        new_node =  tree((new_x, new_y, new_z ))
        new_node.parent = near_node
        return new_node
    
    def calc_dist_theta_phi(self,random_node, near_node):
        dx = random_node.x - near_node.x 
        dy = random_node.y - near_node.y
        dz = random_node.z - near_node.z
        return np.sqrt(dx**2 + dy**2 + dz**2), math.atan2(dy, dx), math.atan2(dz , np.sqrt(dx**2+dy**2))
    
    def compute_path(self, node_end):
        path= []
        node_now = node_end
        while node_now.parent is not None:
            path.append((node_now.x,node_now.y, node_now.z))
            node_now = node_now.parent
        return path[::-1]



        
        