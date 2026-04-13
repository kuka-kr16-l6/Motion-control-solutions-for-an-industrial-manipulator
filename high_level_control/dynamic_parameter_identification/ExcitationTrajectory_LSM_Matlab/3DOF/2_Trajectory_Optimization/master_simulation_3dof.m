%% Master Simulation and Identification Script for 3-DOF KUKA KR 16
clear; clc;

disp('======================================================');
disp('   PHASE 3: Virtual System Identification             ');
disp('======================================================');

% 1. Load the Optimized Trajectory
disp('1. Loading Optimized Trajectory...');
load('Optimized_KUKA_Trajectory.mat', 'A_opt', 't');

% 2. Generate the Kinematic Data (Angles, Velocities, Accelerations)
disp('2. Simulating Robot Movement...');
[q, dq, ddq] = generate_trajectory_3dof(t, A_opt);
num_steps = length(t);

% 3. Define the "True" Base Parameters (Virtual KUKA KR 16)
% Since we don't have the real factory CAD data, we invent a "true" robot 
% to see if our algorithm can successfully guess these exact numbers.
theta_true = [
    15.5;  % Base Param 1 (Mass/Inertia mix)
     2.1;  % Base Param 2
    -0.5;  % ...
     8.4;
     0.1;
     1.2;
     5.5;
    12.0;
    -1.1;
     3.3;
     9.8;
     0.4;
    -2.2;
     4.1;
     7.7   % Base Param 15
];

% 4. Build the massive Regressor Matrix for the whole 10 seconds
disp('3. Building the full Observation Matrix (W)...');
W_tot = zeros(3 * num_steps, 15);
for i = 1:num_steps
    W_instant = calculate_W_matrix(q(:, i), dq(:, i), ddq(:, i));
    start_row = (i - 1) * 3 + 1;
    end_row = i * 3;
    W_tot(start_row:end_row, :) = W_instant;
end

% 5. Calculate the "True" Torques required to move the robot
disp('4. Calculating actual motor torques...');
tau_clean = W_tot * theta_true;

% 6. Inject Virtual Sensor Noise (Simulating the Real World)
disp('5. Injecting 5% random sensor noise into torque readings...');
% We add random spikes and static to the perfect torque data
noise_level = 0.05 * std(tau_clean); 
noise = noise_level .* randn(size(tau_clean));
tau_noisy = tau_clean + noise;

% 7. THE MOMENT OF TRUTH: Least Squares Parameter Extraction
disp('6. Running Least Squares Estimation...');
% This is the golden equation: theta = (W^T * W)^-1 * W^T * tau
theta_estimated = (W_tot' * W_tot) \ (W_tot' * tau_noisy);

% 8. Display the Results!
disp('======================================================');
disp('   IDENTIFICATION RESULTS (True vs. Estimated)        ');
disp('======================================================');
disp('    True Value  |  Estimated  |   Error %');
disp('------------------------------------------------------');
for i = 1:15
    err_pct = abs((theta_true(i) - theta_estimated(i)) / theta_true(i)) * 100;
    fprintf(' P%02d: %8.2f   |  %8.2f   |  %6.2f %%\n', i, theta_true(i), theta_estimated(i), err_pct);
end
disp('======================================================');