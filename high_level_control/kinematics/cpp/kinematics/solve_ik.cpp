// solve_ik.cpp
#include "Robot.h"
#include <cmath>
#include <iostream>
#include <algorithm>
using namespace Eigen;
using std::vector;

static inline double clamp01(double v) {
    return std::max(-1.0, std::min(1.0, v));
}

static inline double normalize_angle(double a) {
    a = fmod(a + M_PI, 2 * M_PI);
    if (a < 0.0) {
        a += 2 * M_PI;
    }
    return a - M_PI;

}

vector<Matrix<double, 6, 1>>
Robot::solve_ik(const vector<double>& position)const {
    Matrix4d T_desired = Transformation(position);

    vector<Matrix<double, 6, 1>> solutions;
    solutions.reserve(8);

    Vector3d p = T_desired.block<3,1>(0,3);
    Matrix3d R = T_desired.block<3,3>(0,0);

    // Wrist center
    Vector3d wc = p - d6 * R.col(2);
    double px = wc(0), py = wc(1), pz = wc(2);

    // Θ1 two solutions
    vector<double> theta1_list;
    double t1a = atan2(py, px);
    theta1_list.push_back(t1a);
    theta1_list.push_back(t1a + M_PI);

    double r = sqrt(px*px + py*py) - a1;
    double s = pz - d1;

    double side_a = d4;
    double side_c = a2;
    double side_b = sqrt(r*r + s*s);

    // Protect acos domain
    double cosA = clamp01((side_b*side_b + side_c*side_c - side_a*side_a) /
                          (2*side_b*side_c));
    double cosB = clamp01((side_a*side_a + side_c*side_c - side_b*side_b) /
                          (2*side_a*side_c));

    double angle_a = acos(cosA);
    double angle_b = acos(cosB);

    double elbow_offset = atan2(-a3, d4);

    double t2a = M_PI/2 - angle_a - atan2(s, r);
    double t2b = M_PI/2 + angle_a - atan2(s, r);

    double t3a = M_PI/2 - (angle_b + elbow_offset);
    double t3b = M_PI/2 - (-angle_b + elbow_offset);

    vector<double> theta2_list = {t2a, t2b};
    vector<double> theta3_list = {t3a, t3b};

    double constexpr  eps = 1e-6;

    for (double t1 : theta1_list) {
        for (int i = 0; i < 2; i++) {

            double t2 = theta2_list[i];
            double t3 = theta3_list[i];

            double t1n = normalize_angle(t1);
            t2 = normalize_angle(t2);
            t3 = normalize_angle(t3);

            Matrix3d R03 = Robot::R03_from_t123(t1n, t2, t3);
            Matrix3d R36;
            R36.noalias() = R03.transpose() * R;

            double ax = R36(0,2);
            double ay = R36(1,2);
            double az = R36(2,2);
            double nz = R36(2,0);
            double sz = R36(2,1);

            double s5 = sqrt(ax*ax + ay*ay);

            if (s5 < eps) {

                double theta_sum = atan2(R36(1,0), R36(0,0)); // θ4 + θ6
                double t4_sing = 0.0;
                double t5_sing = (az >= 0.0 ? 0.0 : M_PI);
                double t6_sing = normalize_angle(theta_sum - t4_sing);

                Matrix<double,6,1> sol;
                sol << t1n, t2, t3, normalize_angle(t4_sing), normalize_angle(t5_sing), normalize_angle(t6_sing);
                if (in_limits(sol))
                    solutions.push_back(sol);
            }
            else {
                double t5_pos = atan2(-s5, az);
                double t4_pos = atan2(ay, ax);
                double t6_pos = atan2(sz, -nz);

                Matrix<double,6,1> sol1;
                sol1 << t1n, t2, t3,
                        normalize_angle(t4_pos),
                        normalize_angle(t5_pos),
                        normalize_angle(t6_pos);
                if (in_limits(sol1))
                    solutions.push_back(sol1);

                double t5_neg = atan2(s5, az);
                double t4_neg = atan2(-ay, -ax);
                double t6_neg = atan2(-sz, nz);

                Matrix<double,6,1> sol2;
                sol2 << t1n, t2, t3,
                        normalize_angle(t4_neg),
                        normalize_angle(t5_neg),
                        normalize_angle(t6_neg);
                if (in_limits(sol2))
                    solutions.push_back(sol2);
            }
        }
    }
    return solutions;
}
