function score = calculate_uncertainty_volume_3dof(A_flat, t, wf)
    % 1. Reshape the flat 33-element array back into a 3x11 matrix
    A_matrix = reshape(A_flat, 3, 11);
    
    % 2. Generate the coupled 3-DOF movements 
    % (CRITICAL FIX: Added wf as the 3rd argument!)
    [q, dq, ddq] = generate_trajectory_3dof(t, A_matrix, wf);
    
    % 3. Preallocate the massive Regressor Matrix for speed
    num_steps = length(t);
    W_tot = zeros(3 * num_steps, 15); 
    
    % 4. Build the Regressor Matrix step-by-step
    for i = 1:num_steps
        q_current = q(:, i);
        dq_current = dq(:, i);
        ddq_current = ddq(:, i);
        
        W_instant = calculate_W_matrix(q_current, dq_current, ddq_current);
        
        start_row = (i - 1) * 3 + 1;
        end_row = i * 3;
        W_tot(start_row:end_row, :) = W_instant;
    end
    
    % 5. Calculate the Information Matrix
    Info = W_tot' * W_tot;
    
    % 6. The Log-Determinant Trick
    score = -log(det(Info)); 
    
    % Safety Net
    if isinf(score) || ~isreal(score)
        score = 1e6; 
    end
end