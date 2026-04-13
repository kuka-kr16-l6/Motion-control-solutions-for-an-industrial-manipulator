function [W_base, theta_base, W_standard] = extract_base_parameters(tau, q, dq, ddq, theta_standard)
    % Extracts the Regressor Matrix and reduces it to the Base Parameters.
    
    disp('   -> Extracting Standard Regressor Matrix (W)...');
    % 1. Pull the 30 parameters out of the torque equations
    W_standard = equationsToMatrix([tau(1); tau(2); tau(3)], theta_standard);
    
    disp('   -> Identifying Base Parameters (The Hybrid Trick)...');
    % 2. Create an empty numerical observation matrix
    W_numeric = zeros(30, 30); 
    
    % NEW: We must declare the leftover symbols so we can substitute them
    syms g L3 real
    
    for k = 1:10
        % Generate random joint angles, velocities, and accelerations
        q_rand = rand(3,1);
        dq_rand = rand(3,1);
        ddq_rand = rand(3,1);
        
        % NEW: Define numerical values for gravity and the wrist length
        g_num = 9.81;
        L3_num = 0.15; % Assuming the payload center is 15cm from the elbow
        
        % Substitute ALL symbols into numbers
        W_eval = double(subs(W_standard, ...
            [q; dq; ddq; g; L3], ...
            [q_rand; dq_rand; ddq_rand; g_num; L3_num]));
        
        % Stack the 3x30 matrices vertically into our 30x30 numeric grid
        start_row = (k-1)*3 + 1;
        W_numeric(start_row:start_row+2, :) = W_eval;
    end
    
    disp('   -> Running QR Decomposition...');
    % 3. Find the independent columns using numeric QR decomposition
    [~, ~, P] = qr(W_numeric, 'vector');
    
    % Calculate exactly how many columns actually matter
    tolerance = 1e-6;
    rank_W = rank(W_numeric, tolerance);
    
    % Sort the "good" column indices back into numerical order
    independent_cols = sort(P(1:rank_W));
    
    disp(['   -> Success! Reduced from 30 parameters down to ', num2str(rank_W), ' Base Parameters.']);
    
    % 4. Create the final, optimized Base Parameter symbolic arrays
    W_base = W_standard(:, independent_cols);
    theta_base = theta_standard(independent_cols);
    
end