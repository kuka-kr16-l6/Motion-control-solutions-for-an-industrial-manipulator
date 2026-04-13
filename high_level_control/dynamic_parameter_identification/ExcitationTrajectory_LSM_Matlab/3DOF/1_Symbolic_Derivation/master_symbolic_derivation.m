%% Master Symbolic Derivation Script for 3-DOF KUKA KR 16 L6
% Run this script ONCE to generate the Base Parameter equations.
clear; clc;
disp('======================================================');
disp('   Starting 3-DOF Symbolic Derivation (KUKA KR 16)    ');
disp('======================================================');
tic; % Start a timer to see how long the derivation takes

%% Step 1: Define all Symbolic Variables
disp('1. Initializing Symbols...');
[q, dq, ddq, theta_standard, params] = define_kuka_symbols();

%% Step 2: Calculate Kinematics (DH Transformations)
disp('2. Building Kinematic Chain...');
[T01, T02, T03] = build_kuka_kinematics(q, params);

%% Step 3: Energy and Torques (Euler-Lagrange)
disp('3. Calculating Dynamics (This may take a few minutes)...');
tau = calculate_symbolic_torques(q, dq, ddq, T01, T02, T03, theta_standard);

%% Step 4: Base Parameter Extraction
disp('4. Extracting Base Parameter Regressor Matrix (W)...');
[W_base, theta_base, W_standard] = extract_base_parameters(tau, q, dq, ddq, theta_standard);

%% Step 5: Save the Results and Generate Function!
% Define the exact destination folder
target_folder = '../2_Trajectory_Optimization/';

disp(['5. Saving derived equations directly to ', target_folder, '...']);
save([target_folder, 'KUKA_Base_Parameters.mat'], 'W_base', 'theta_base', 'W_standard', 'tau', 'q', 'dq', 'ddq');

disp('6. Injecting constants and writing fast numerical function...');
syms g L3 real
W_base_compiled = subs(W_base, [g; L3], [9.81; 0.15]);

% Tell MATLAB to build the file inside Folder 2
matlabFunction(W_base_compiled, 'File', [target_folder, 'calculate_W_matrix'], 'Vars', {q, dq, ddq});
disp('   -> Success! The W matrix has been delivered to Folder 2.');

elapsed_time = toc; % Stop the timer
disp('======================================================');
disp(['   Derivation Complete in ', num2str(elapsed_time), ' seconds!']);
disp('======================================================');