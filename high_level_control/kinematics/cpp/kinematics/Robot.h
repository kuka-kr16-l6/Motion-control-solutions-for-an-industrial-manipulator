//
// Created by mahmoud on 11/23/2025.
//
#ifndef ROBOT_H
#define ROBOT_H

#include <Eigen/Dense>
#include <vector>
using namespace Eigen;
using namespace std;
using std::vector;

// constexpr double POS_ERROR_THRESHOLD = 1e-3;
// constexpr double ROT_ERROR_THRESHOLD = 1e-6;

class Robot {
public:
    double d1, d4, d6;
    double a1, a2, a3;
    Vector3d g0;
    vector<pair<double, double>> joint_limits;
    Robot();


    [[nodiscard]]
    Matrix4d tf_matrix(double alpha, double a, double d, double theta) const;

    [[nodiscard]]
    vector<Matrix<double, 6, 1>> solve_ik(const vector<double>& position)const ;

    [[nodiscard]]
    static Matrix4d Transformation(const vector<double>& position) {
        Matrix3d R = Robot::rpy_to_rot(position[3], position[4], position[5]);

        Matrix4d T = Matrix4d::Identity();
        T.block<3,3>(0,0) = R;
        T.block<3,1>(0,3) = Vector3d(position[0], position[1], position[2]);
        return T;
    }
    static Matrix3d rpy_to_rot(double roll, double pitch, double yaw) {
        Matrix3d Rz, Ry, Rx;

        Rz << cos(yaw), -sin(yaw), 0,
              sin(yaw),  cos(yaw), 0,
                    0,        0, 1;

        Ry << cos(pitch), 0, sin(pitch),
                        0, 1,          0,
        -sin(pitch), 0, cos(pitch);

        Rx << 1,     0,              0,
              0,     cos(roll), -sin(roll),
              0,     sin(roll),  cos(roll);

        return Rz * Ry * Rx;
    }
    static inline Matrix3d R03_from_t123(double t1, double t2, double t3) {
        using std::sin;
        using std::cos;
        double c1 = cos(t1);
        double s1 = sin(t1);
        double alpha = t2 + t3;
        double s_alpha = sin(alpha);
        double c_alpha = cos(alpha);

        Matrix3d R03;
        R03(0,0) = c1 * s_alpha;  R03(0,1) = s1;    R03(0,2) = c1 * c_alpha;
        R03(1,0) = s1 * s_alpha;  R03(1,1) = -c1;   R03(1,2) = s1 * c_alpha;
        R03(2,0) = c_alpha;        R03(2,1) = 0.0;   R03(2,2) = -s_alpha;
        return R03;
    }

    [[nodiscard]]
    bool in_limits(const Matrix<double, 6, 1>& q) const {
        for (int i = 0; i < 6; i++) {
            double qi = q(i);
            double qmin = joint_limits[i].first;
            double qmax = joint_limits[i].second;
            if (qi < qmin  || qi > qmax ) {
                return false;
            }

        }
        return true;
    }

    [[nodiscard]]
    Matrix4d forward_kinematics(const Eigen::Matrix<double, 6, 1>& q) const;

};

#endif //ROBOT_H