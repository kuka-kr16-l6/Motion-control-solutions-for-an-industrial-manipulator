cmake_minimum_required(VERSION 4.0)
project(kinematics)

set(CMAKE_CXX_STANDARD 20)
set(EIGEN3_INCLUDE_DIR "C:/toolbox/eigen-5.0.0")
include_directories(${EIGEN3_INCLUDE_DIR})
add_executable(kinematics main.cpp
        Robot.cpp
        Robot.h
        solve_ik.cpp
)
