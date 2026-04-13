function tau = calculate_symbolic_torques(q, dq, ddq, T01, T02, T03, theta_standard)
    % Calculates the dynamic torques using linear-parameterized Euler-Lagrange
    
    syms g real 
    
    %% 1. Extract Mass, First Moment of Mass (l), and Inertia (I)

    disp('   -> Extracting Linear Parameters...');

    m1 = theta_standard(1); l1 = theta_standard(2:4);
    I1 = [theta_standard(5), theta_standard(8), theta_standard(9);
          theta_standard(8), theta_standard(6), theta_standard(10);
          theta_standard(9), theta_standard(10), theta_standard(7)];
      
    m2 = theta_standard(11); l2 = theta_standard(12:14);
    I2 = [theta_standard(15), theta_standard(18), theta_standard(19);
          theta_standard(18), theta_standard(16), theta_standard(20);
          theta_standard(19), theta_standard(20), theta_standard(17)];
      
    m3 = theta_standard(21); l3 = theta_standard(22:24);
    I3 = [theta_standard(25), theta_standard(28), theta_standard(29);
          theta_standard(28), theta_standard(26), theta_standard(30);
          theta_standard(29), theta_standard(30), theta_standard(27)];

    %% 2. Extract Rotation (R) and Position (p) of the Joint Hinges

    disp('   -> Calculating Kinematics at Joint Origins...');
    
    R1 = T01(1:3, 1:3); p1 = T01(1:3, 4);
    R2 = T02(1:3, 1:3); p2 = T02(1:3, 4);
    R3 = T03(1:3, 1:3); p3 = T03(1:3, 4);

    %% 3. Calculate Linear Velocities of the Hinges
    v1 = jacobian(p1, q) * dq;
    v2 = jacobian(p2, q) * dq;
    v3 = jacobian(p3, q) * dq;

    %% 4. Calculate Angular Velocities
    Z0 = [0; 0; 1];
    w1 = Z0 * dq(1);
    w2 = w1 + T01(1:3, 3) * dq(2);
    w3 = w2 + T02(1:3, 3) * dq(3);

    %% 5. Rotate velocities into LOCAL link frames (Crucial for linearity!)
    v1_loc = R1.' * v1; w1_loc = R1.' * w1;
    v2_loc = R2.' * v2; w2_loc = R2.' * w2;
    v3_loc = R3.' * v3; w3_loc = R3.' * w3;

    %% 6. Kinetic Energy (Linearized Formulation)

    disp('   -> Calculating Strictly Linear Energies...');
    
    K1 = 0.5*m1*(v1_loc.' * v1_loc) + v1_loc.' * cross(w1_loc, l1) + 0.5*w1_loc.' * I1 * w1_loc;
    K2 = 0.5*m2*(v2_loc.' * v2_loc) + v2_loc.' * cross(w2_loc, l2) + 0.5*w2_loc.' * I2 * w2_loc;
    K3 = 0.5*m3*(v3_loc.' * v3_loc) + v3_loc.' * cross(w3_loc, l3) + 0.5*w3_loc.' * I3 * w3_loc;
    K_total = K1 + K2 + K3;

    %% 7. Potential Energy (Linearized: m*g*z + local mass moment rotated to global Z)
    g_vec = [0; 0; g]; 
    P1_pot = g_vec.' * (m1 * p1 + R1 * l1);
    P2_pot = g_vec.' * (m2 * p2 + R2 * l2);
    P3_pot = g_vec.' * (m3 * p3 + R3 * l3);
    P_total = P1_pot + P2_pot + P3_pot;

    L = simplify(K_total - P_total);

    %% 8. Apply Euler-Lagrange Equation

    disp('   -> Running Euler-Lagrange Derivatives (This takes the longest)...');
    
    tau = sym(zeros(3,1));
    for i = 1:3
        dL_ddq = jacobian(L, dq(i));
        d_dt_term = jacobian(dL_ddq, q) * dq + jacobian(dL_ddq, dq) * ddq;
        dL_dq = jacobian(L, q(i));
        tau(i) = simplify(d_dt_term - dL_dq);
    end
end