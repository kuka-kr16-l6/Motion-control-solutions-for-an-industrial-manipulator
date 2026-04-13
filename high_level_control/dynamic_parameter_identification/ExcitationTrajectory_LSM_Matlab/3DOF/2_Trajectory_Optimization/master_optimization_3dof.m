%% Master Optimization Script for 3-DOF KUKA KR 16 L6
% Phase 2: Trajectory Optimization (Swevers Method)
clear; clc; close all;

disp('======================================================');
disp('   PHASE 2: Optimal Trajectory Generation             ');
disp('======================================================');

%% 1. Define the Timeline and Frequency
disp('Setting up timing and Fourier parameters...');
% 10 seconds of movement, sampled at 100 Hz (1000 snapshots)
t = linspace(0, 10, 1000); 

% The Swevers paper uses a 0.1 Hz fundamental frequency
f = 0.1;                   
wf = 2 * pi * f;           % Fundamental pulsation in rad/s

%% 2. Set up the 33 Dials (11 harmonics * 3 joints)
disp('Initializing the 33 trajectory coefficients...');
% Using small random numbers instead of ones to break mathematical symmetry 
% and give the optimizer a better starting landscape.
A_initial_flat = 0.1 * randn(1, 33); 

% Hard mathematical bounds for the coefficients (a_l and b_l)
lb = -5 * ones(1, 33); 
ub =  5 * ones(1, 33); 

%% 3. Configure the Optimizer (fmincon)
options = optimoptions('fmincon', ...
    'Display', 'iter', ...           % Show the step-by-step table
    'Algorithm', 'sqp', ...          % Sequential Quadratic Programming (Industry standard)
    'MaxFunctionEvaluations', 50000, ...
    'MaxIterations', 2000, ...
    'StepTolerance', 1e-6);

%% 4. Define the Anonymous Functions
% We wrap our custom functions so fmincon only "sees" the variable 'A'
objective_fun = @(A) calculate_uncertainty_volume_3dof(A, t, wf);
constraint_fun = @(A) kuka_kinematic_constraints(A, t, wf);

disp('Launching fmincon! Watch the objective value (Fval) drop...');

%% 5. Run the Optimization!
% fmincon(fun, x0, A, b, Aeq, beq, lb, ub, nonlcon, options)
A_opt_flat = fmincon(objective_fun, A_initial_flat, ...
                     [], [], [], [], lb, ub, constraint_fun, options);

%% 6. Process and Save the Results
% Reshape the final optimized array back into a usable 3x11 matrix
A_opt = reshape(A_opt_flat, 3, 11);

disp('======================================================');
disp('   Optimization Complete!                             ');
disp('======================================================');

% Save the perfect trajectory dials for Phase 3 (Data Collection)
save('Optimized_KUKA_Trajectory.mat', 'A_opt', 't', 'wf');
disp('Saved A_opt to Optimized_KUKA_Trajectory.mat');

% --- Helper Function for Kinematic Constraints ---
function [c, ceq] = kuka_kinematic_constraints(A_flat, t, wf)
    % c <= 0    (Nonlinear inequalities - e.g., speed limits)
    % ceq == 0  (Nonlinear equalities - not used here)
    ceq = []; 
    
    % Reshape and generate the proposed trajectory
    A_matrix = reshape(A_flat, 3, 11);
    [q, dq, ddq] = generate_trajectory_3dof(t, A_matrix, wf);
    
    % KUKA KR 16 Joint Limits (Convert your manual's degrees to radians!)
    % Example limits (Make sure these match your specific robot):
    q_max  = [ 3.22;  2.70;  2.70]; % Position upper limits (rad)
    q_min  = [-3.22; -2.70; -2.70]; % Position lower limits (rad)
    dq_max = [ 2.72;  2.72;  2.72]; % Max Velocity (rad/s)
    ddq_max= [ 5.00;  5.00;  5.00]; % Max Acceleration (rad/s^2)
    
    % Initialize empty arrays for the violations
    c_q_upper = []; c_q_lower = [];
    c_dq      = []; c_ddq     = [];
    
    % Loop through all 3 joints to check every single millisecond
    for i = 1:3
        % Position limits
        c_q_upper = [c_q_upper, max(q(i, :)) - q_max(i)];
        c_q_lower = [c_q_lower, q_min(i) - min(q(i, :))];
        
        % Velocity limits (absolute value because it spins both ways)
        c_dq = [c_dq, max(abs(dq(i, :))) - dq_max(i)];
        
        % Acceleration limits
        c_ddq = [c_ddq, max(abs(ddq(i, :))) - ddq_max(i)];
    end
    
    % Combine all constraint checks into one vector 'c'. 
    % fmincon will aggressively force EVERY number in this vector to be <= 0.
    c = [c_q_upper, c_q_lower, c_dq, c_ddq];
end