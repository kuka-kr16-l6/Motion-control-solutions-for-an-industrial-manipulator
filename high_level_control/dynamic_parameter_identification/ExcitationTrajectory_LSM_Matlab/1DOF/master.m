%% Step 1: The Setup

t = linspace(0, 10, 1500); 
theta_true = [1.5; 0.5; 0.1]; % Our secret Inertia, Gravity, Friction
A_initial = ones(1, 11);      % The starting point for our 11 dials

%% Step 2: The Optimizer (Chapter 1)

% Set limits so the robot doesn't swing too violently (e.g., max amplitude of 5)
lower_bounds = -5 * ones(1, 11);
upper_bounds =  5 * ones(1, 11);

% Run the Optimizer! It goes to sleep once it outputs 'A_opt'
options = optimoptions('fmincon', 'Display', 'iter');
A_opt = fmincon(@(A) calculate_uncertainty_volume(A, t), ...
                     A_initial, ...
                     [], [], [], [], ...
                     lower_bounds, ...
                     upper_bounds, ...
                     [], ...
                     options);

%% Step 3: The Virtual Run (Chapter 2 - Part 1)

% Make the virtual robot run the perfect course
[q, dq, ddq] = generate_trajectory(t, A_opt);

% Calculate the theoretical torque and inject messy real-world noise
tau = calculate_torque(q, dq, ddq, theta_true);
noisy_tau = tau + randn(size(tau));

%% Step 4: The Evaluator (Chapter 2 - Part 2)

W = [ddq', sin(q)', dq'];

% Calculate the final guess using the Least Squares formula!
theta_guess = inv(W' * W) * W' * noisy_tau';

% Print the results to the screen to compare!
disp('--- RESULTS ---');
disp('True Parameters:');
disp(theta_true);
disp('Guessed Parameters:');
disp(theta_guess);

%% Step 5: Visualize the Optimized Trajectory
% 1. Run the generator one last time using the perfect, optimized dials
[q_opt, dq_opt, ddq_opt] = generate_trajectory(t, A_opt);

% 2. Create a large, clean figure window
figure('Name', 'Optimized Robot Trajectory', 'Color', 'w');

% 3. Plot Position (q) - The actual physical angle of the arm
subplot(3, 1, 1);
plot(t, q_opt, 'b', 'LineWidth', 1.5);
title('Position (Angle) over Time');
ylabel('q (rad)');
grid on;

% 4. Plot Velocity (dq) - How fast it swings
subplot(3, 1, 2);
plot(t, dq_opt, 'r', 'LineWidth', 1.5);
title('Velocity over Time');
ylabel('dq (rad/s)');
grid on;

% 5. Plot Acceleration (ddq) - The sudden jerks and stops
subplot(3, 1, 3);
plot(t, ddq_opt, 'k', 'LineWidth', 1.5);
title('Acceleration over Time');
xlabel('Time (seconds)');
ylabel('ddq (rad/s^2)');
grid on;