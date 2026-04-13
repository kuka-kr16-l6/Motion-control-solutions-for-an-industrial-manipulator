function [T01, T02, T03] = build_kuka_kinematics(q, params)
    % Calculates the absolute Denavit-Hartenberg transformation matrices
    
    % DH Matrix Generator (Anonymous Function)
    dh = @(a, alpha, d, theta) ...
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta);
         sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta);
         0,           sin(alpha),             cos(alpha),            d;
         0,           0,                      0,                     1];
     
    % Joint 1: Base to Shoulder. Twists -90 deg to lay Z-axis flat.
    T01 = dh(params.L1_x, -pi/2, params.L1_z, q(1));
    
    % Joint 2: Shoulder to Elbow. No twist. KUKA stands straight at 0 deg, so subtract pi/2.
    T12 = dh(params.L2, 0, 0, q(2) - pi/2);
    
    % Joint 3: Elbow to Wrist. No twist.
    T23 = dh(params.L3, 0, 0, q(3));
    
    % Calculate absolute frames from the base (simplify cleans up the trig math)
    T02 = simplify(T01 * T12);
    T03 = simplify(T02 * T23);
end