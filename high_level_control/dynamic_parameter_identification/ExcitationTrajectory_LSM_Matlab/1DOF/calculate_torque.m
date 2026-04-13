function tau = calculate_torque(q, dq, ddq, theta)
% Calculates the torque according to its physics
% theta(1) = inertia, theta(2) = gravity, theta(3) = friction
arguments (Input)
    q (1,:) double
    dq (1,:) double
    ddq (1,:) double
    theta (:,1) double
end

arguments (Output)
    tau (1,:) double
end

    inertia_torque = theta(1) * ddq;
    gravity_torque = theta(2) * sin(q);
    friction_torque = theta(3) * dq;

    tau = inertia_torque + gravity_torque + friction_torque;
end