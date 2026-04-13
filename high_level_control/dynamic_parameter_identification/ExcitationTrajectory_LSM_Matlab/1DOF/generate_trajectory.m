function [q, dq, ddq] = generate_trajectory(t, A)
% This function will take a time array (t) and our dial setting (A), and output the movement data

arguments (Input)
    t (1,:) double
    A (1,:) double
end

arguments (Output)
    q (1,:) double
    dq (1,:) double
    ddq (1,:) double
end

%% 1. Create a blank timeline filled with zeros (our empty master track)

    q = zeros(size(t));
    dq = zeros(size(t));
    ddq = zeros(size(t));

%% 2. Start a loop to check all 11 sliders one by one and stack the waves.

    for k = 1:11
        % Position: Add the current wave
        q = q + A(k) * sin(k * t);
        
        % Velocity: Derivative of sine is cosine. The chain rule pulls out one 'k'
        dq = dq + A(k) * k * cos(k * t);
        
        % Acceleration: Derivative of cosine is negative sine. The chain rule pulls out a second 'k'
        ddq = ddq - A(k) * k^2 * sin(k * t);
    end
end