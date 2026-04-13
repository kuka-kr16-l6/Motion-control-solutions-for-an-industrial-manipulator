function [q, dq, ddq, theta_standard, params] = define_kuka_symbols()
    % Defines all symbolic variables for the 3-DOF system
    
    syms q1 q2 q3 dq1 dq2 dq3 ddq1 ddq2 ddq3 real
    q = [q1; q2; q3];
    dq = [dq1; dq2; dq3];
    ddq = [ddq1; ddq2; ddq3];
    
    % Link 1 Parameters (Using First Moment of Mass: mx, my, mz)
    syms m1 mx1 my1 mz1 Ixx1 Iyy1 Izz1 Ixy1 Ixz1 Iyz1 real
    % Link 2 Parameters
    syms m2 mx2 my2 mz2 Ixx2 Iyy2 Izz2 Ixy2 Ixz2 Iyz2 real
    % Link 3 Parameters 
    syms m3 mx3 my3 mz3 Ixx3 Iyy3 Izz3 Ixy3 Ixz3 Iyz3 real
    
    % The strictly linear 30-parameter vector
    theta_standard = [m1; mx1; my1; mz1; Ixx1; Iyy1; Izz1; Ixy1; Ixz1; Iyz1; ...
                      m2; mx2; my2; mz2; Ixx2; Iyy2; Izz2; Ixy2; Ixz2; Iyz2; ...
                      m3; mx3; my3; mz3; Ixx3; Iyy3; Izz3; Ixy3; Ixz3; Iyz3];
                  
    params.L1_x = 0.260; 
    params.L1_z = 0.675; 
    params.L2   = 0.705; 
    syms L3 real         
    params.L3   = L3;    
end