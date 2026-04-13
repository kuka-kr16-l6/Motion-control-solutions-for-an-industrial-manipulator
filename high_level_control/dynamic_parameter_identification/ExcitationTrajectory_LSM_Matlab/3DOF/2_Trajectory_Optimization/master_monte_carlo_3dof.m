%% Monte Carlo Analysis for 3-DOF KUKA Identification
clear; clc;
disp('======================================================');
disp('   PHASE 4: Monte Carlo Robustness Analysis           ');
disp('======================================================');

% 1. Setup
load('Optimized_KUKA_Trajectory.mat', 'A_opt', 't');
[q, dq, ddq] = generate_trajectory_3dof(t, A_opt);
num_steps = length(t);
num_trials = 200; % We will run the experiment 100 times

% "True" KUKA Parameters
theta_true = [15.5; 2.1; -0.5; 8.4; 0.1; 1.2; 5.5; 12.0; -1.1; 3.3; 9.8; 0.4; -2.2; 4.1; 7.7];

% 2. Pre-build the W matrix (It's the same for every trial!)
disp('Building the Regressor Matrix once...');
W_tot = zeros(3 * num_steps, 15);
for i = 1:num_steps
    W_tot((i-1)*3+1 : i*3, :) = calculate_W_matrix(q(:,i), dq(:,i), ddq(:,i));
end
tau_clean = W_tot * theta_true;

% 3. Run the Monte Carlo Loop
all_estimates = zeros(15, num_trials);
disp(['Running ', num2str(num_trials), ' noisy experiments...']);

for n = 1:num_trials
    % Inject 5% random noise (unique for every trial)
    noise = (0.05 * std(tau_clean)) .* randn(size(tau_clean));
    tau_noisy = tau_clean + noise;
    
    % Identify parameters for this specific trial
    all_estimates(:, n) = (W_tot' * W_tot) \ (W_tot' * tau_noisy);
    
    if mod(n, 10) == 0, fprintf('Trial %d/100...\n', n); end
end

% 4. Calculate Statistical Results
mean_estimates = mean(all_estimates, 2);
std_estimates = std(all_estimates, 0, 2);
mean_error_pct = abs((theta_true - mean_estimates) ./ theta_true) * 100;

% 5. Professional Results Table
disp('======================================================');
disp('   MONTE CARLO RESULTS (100 Trials at 5% Noise)       ');
disp('======================================================');
fprintf('%-6s | %-10s | %-10s | %-8s\n', 'Param', 'True Val', 'Mean Est', 'Avg Err%');
disp('------------------------------------------------------');
for i = 1:15
    fprintf('P%02d    | %10.2f | %10.2f | %7.2f%%\n', ...
        i, theta_true(i), mean_estimates(i), mean_error_pct(i));
end

% 6. Visualization: The Error Histogram
figure('Color', 'w', 'Name', 'Monte Carlo Parameter Distribution');
subplot(2,1,1);
histogram(all_estimates(8,:), 15, 'FaceColor', [0 0.45 0.74]);
title('Distribution for Large Parameter (P08)');
xlabel('Estimated Value'); ylabel('Frequency');
grid on;

subplot(2,1,2);
histogram(all_estimates(5,:), 15, 'FaceColor', [0.85 0.33 0.1]);
title('Distribution for Small/Noisy Parameter (P05)');
xlabel('Estimated Value'); ylabel('Frequency');
grid on;