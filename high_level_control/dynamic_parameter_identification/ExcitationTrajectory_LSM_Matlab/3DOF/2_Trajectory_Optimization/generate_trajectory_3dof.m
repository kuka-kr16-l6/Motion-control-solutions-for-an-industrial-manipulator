function [q, dq, ddq] = generate_trajectory_3dof(t, params_matrix, wf)
    % GENERATE_TRAJECTORY_3DOF Calculates joint trajectories based on Fourier Series
    %
    % INPUTS:
    % t             : Time vector (e.g., 0:0.01:10)
    % params_matrix : 3x11 matrix containing the optimized variables.
    %                 Cols 1-5  : 'a' coefficients (a_1 to a_5)
    %                 Cols 6-10 : 'b' coefficients (b_1 to b_5)
    %                 Col 11    : 'q0' position offset
    % wf            : Fundamental pulsation (omega_f) in rad/s.
    
    num_time_steps = length(t);
    q = zeros(3, num_time_steps);
    dq = zeros(3, num_time_steps);
    ddq = zeros(3, num_time_steps);
    
    N = 5; % Number of harmonics (Ni in the equation)
    
    % Loop through each joint (1, 2, and 3)
    for i = 1:3
        % Extract the position offset (qi0) for this joint
        qi0 = params_matrix(i, 11);
        
        % Initialize position with the offset
        q(i, :) = qi0 * ones(1, num_time_steps);
        
        % Loop through the 5 Fourier harmonics (l = 1 to Ni)
        for l = 1:N
            % Extract a_l and b_l coefficients from the matrix
            a_l = params_matrix(i, l);
            b_l = params_matrix(i, l + N); 
            
            % 1. Position Equation: q_i(t)
            q(i, :) = q(i, :) + (a_l / (wf * l)) * sin(wf * l * t) ...
                              - (b_l / (wf * l)) * cos(wf * l * t);
            
            % 2. Velocity Equation: dq_i(t)
            dq(i, :) = dq(i, :) + a_l * cos(wf * l * t) ...
                                + b_l * sin(wf * l * t);
            
            % 3. Acceleration Equation: ddq_i(t)
            % Note: Image has a typo 'a_k' instead of 'a_l', but the math is a_l
            ddq(i, :) = ddq(i, :) - a_l * (wf * l) * sin(wf * l * t) ...
                                  + b_l * (wf * l) * cos(wf * l * t);
        end
    end
end