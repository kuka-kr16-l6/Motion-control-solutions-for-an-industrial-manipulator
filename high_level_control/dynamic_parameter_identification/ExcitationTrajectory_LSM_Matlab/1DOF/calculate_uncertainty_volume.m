function volume = calculate_uncertainty_volume(A, t)
% This function is the "calculator" fmincon uses to grade the trajectory.
% It outputs a single number: the volume of the uncertainty bubble.

arguments (Input)
    A (1,:) double
    t (1,:) double
end
arguments (Output)
    volume (1,1) double
end

    % 1. Do a dry run of the movement using the current dial settings
    [q, dq, ddq] = generate_trajectory(t, A);
    
    % 2. Build the temporary Regressor Matrix (the obstacle course)
    W = [ddq', sin(q)', dq'];
    
    % 3. Calculate the Information Matrix (the scorecard)
    Info = W' * W;
    
    % 4. Calculate the Volume of the Uncertainty Bubble!
    % fmincon's entire goal is to crush this single number down to zero.
    volume = -log(det(Info)); 
    
end