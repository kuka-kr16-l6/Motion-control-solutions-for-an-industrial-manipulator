#include <iostream>
#include <chrono>
#include "Robot.h"

using namespace std;
using namespace Eigen;

inline double rad2deg(double rad) {
    return rad * 180.0 / M_PI;
}

int main() {

    Robot kuka;

    double px = 0.7;
    double py = 1.0;
    double pz = 0.3;

    double roll = 30 * M_PI/ 180.0;
    double pitch = 40 * M_PI/ 180.0;
    double yaw = 50 * M_PI/ 180.0;
    vector<double> position = {px, py, pz, roll, pitch,yaw};

    cout << "Desired Position: " << px << ", " << py << ", " << pz << endl;
    cout << "Desired RPY (deg): "
         << rad2deg(roll) << ", "
         << rad2deg(pitch) << ", "
         << rad2deg(yaw) << endl << endl;

    // time
    auto start = chrono::high_resolution_clock::now();
    vector<Matrix<double, 6, 1>> sols = kuka.solve_ik(position);
    auto end = chrono::high_resolution_clock::now();

    double elapsed_ms = chrono::duration<double, milli>(end - start).count();
    double elapsed_us = chrono::duration<double, micro>(end - start).count();

    cout << "Found " << sols.size() << " IK solutions" << endl;
    cout << "IK Time: " << elapsed_ms << " ms  (" << elapsed_us << " us)" << endl << endl;


    // ======== VALIDATE RESULTS USING FK ========
    if (sols.empty()) {
        cout << "No valid IK solutions found." << endl;
        return 0;
    }

    for (size_t i = 0; i < sols.size(); ++i) {

        cout << "--------------- Solution " << (i + 1) << " ---------------" << endl;

        // Print in degrees
        cout << "Joint angles (deg): ";
        for (int j = 0; j < 6; j++) {
            cout << (sols[i](j)) << "  ";
        }
        cout << endl;

        // Compute forward kinematics to verify solution
        Matrix4d Tcheck = kuka.forward_kinematics(sols[i]);
        Matrix4d T = Robot::Transformation(position);

        double pos_err = (Tcheck.block<3,1>(0,3) - T.block<3,1>(0,3)).norm();
        double rot_err = (Tcheck.block<3,3>(0,0) - T.block<3,3>(0,0)).norm();

        cout << "Position error: " << pos_err << endl;
        cout << "Rotation error: " << rot_err << endl;

        // Joint-limit check
        bool ok = true;
        for (int j = 0; j < 6; j++) {
            double q = sols[i](j);
            if (q < kuka.joint_limits[j].first || q > kuka.joint_limits[j].second)
                ok = false;
        }

        cout << "Inside joint limits?  " << (ok ? "YES" : "NO") << endl;
        cout << endl;
    }

    return 0;
}
