cmake_minimum_required(VERSION 3.25)
project(test CUDA)

set(CMAKE_CUDA_STANDARD 14)

add_executable(test main.cu)

set_target_properties(test PROPERTIES
        CUDA_SEPARABLE_COMPILATION ON)
