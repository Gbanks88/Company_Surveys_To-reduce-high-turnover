#!/bin/bash

# Create build directory if it doesn't exist
mkdir -p build
cd build

# Install dependencies with Conan
conan install .. --output-folder=. --build=missing

# Configure with CMake
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake

# Build
cmake --build . -j$(nproc)

# Run tests
ctest --output-on-failure
