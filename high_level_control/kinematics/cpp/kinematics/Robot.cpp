//
// Created by mahmoud on 11/23/2025.
//
#include "Robot.h"
Robot::Robot() {
    // Link offsets / DH parameters
    d1 = 0.675;
    d4 = 0.970;
    d6 = 0.115;

    a1 = 0.260;
    a2 = 0.680;
    a3 = -0.035;

    g0 = Eigen::Vector3d(0.0, 0.0, -9.81);

    joint_limits = {
        {-M_PI_2, M_PI_2},
        { -1.1344, 2.18166 },
        { -3.8397, 1.117 },
        { -6.1086, 6.1086 },
        { -2.268, 2.268 },
        { -6.1086, 6.1086 }
    };
}
inline Matrix4d Robot::tf_matrix(double alpha, double a, double d, double theta) const {
    Matrix4d T = Matrix4d::Identity();
    double ca = cos(alpha);
    double sa = sin(alpha);
    double ct = cos(theta);
    double st = sin(theta);

    T(0,0) = ct;     T(0,1) = -st * ca;   T(0,2) = st * sa;    T(0,3) = a * ct;
    T(1,0) = st;     T(1,1) = ct * ca;    T(1,2) = -ct * sa;   T(1,3) = a * st;
    T(2,0) = 0.0;    T(2,1) = sa;         T(2,2) = ca;         T(2,3) = d;
    T(3,0) = 0.0;    T(3,1) = 0.0;        T(3,2) = 0.0;        T(3,3) = 1.0;

    return T;
}
Matrix4d Robot::forward_kinematics(const Matrix<double,6,1>& q) const
{
    double t1 = q(0);
    double t2 = q(1);
    double t3 = q(2);
    double t4 = q(3);
    double t5 = q(4);
    double t6 = q(5);

    Matrix4d T1 = tf_matrix(-M_PI_2, a1, d1, t1);
    Matrix4d T2 = tf_matrix(0,       a2, 0,  t2 - M_PI_2);
    Matrix4d T3 = tf_matrix(-M_PI_2, a3, 0,  t3);
    Matrix4d T4 = tf_matrix( M_PI_2, 0,  d4, t4);
    Matrix4d T5 = tf_matrix(-M_PI_2, 0,  0,  t5);
    Matrix4d T6 = tf_matrix(0,       0,  d6, t6);

    Matrix4d T = T1 * T2 * T3 * T4 * T5 * T6;
    return T;
}

