%% Master Optimization Script for 3-DOF KUKA KR 16 L6
clear; clc;

disp('======================================================');
disp('   Starting 3-DOF Trajectory Optimization             ');
disp('======================================================');

% 1. Define the Time Vector (10 seconds, 1000 snapshots)
t = linspace(0, 10, 1000);

% 2. Set up the 33 Dials (11 harmonics * 3 joints)
% We start with all dials set to 1
A_initial_flat = ones(1, 33);

% Set the physical limits of the robot (-5 to 5 for every single dial)
lb = -5 * ones(1, 33); 
ub =  5 * ones(1, 33); 

% 3. Configure the Optimizer
% We give it a high evaluation limit because 33 variables is a massive search space
options = optimoptions('fmincon', ...
    'Display', 'iter', ...
    'Algorithm', 'sqp', ... 
    'MaxFunctionEvaluations', 30000, ...
    'MaxIterations', 1000);

disp('Launching fmincon! Watch the score drop...');

% 4. Run the Optimization!
A_opt_flat = fmincon(@(A) calculate_uncertainty_volume_3dof(A, t), ...
    A_initial_flat, [], [], [], [], lb, ub, [], options);

% 5. Reshape the final optimized array back into a usable 3x11 matrix
A_opt = reshape(A_opt_flat, 3, 11);

disp('======================================================');
disp('   Optimization Complete!                             ');
disp('======================================================');

% Save the perfect trajectory dials so you never have to optimize again!
save('Optimized_KUKA_Trajectory.mat', 'A_opt', 't');
disp('Saved A_opt to Optimized_KUKA_Trajectory.mat');