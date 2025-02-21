#!/bin/bash

# Create directory structure
mkdir -p include/{core,db,gui,api,simulation}
mkdir -p src/{core,db,gui,api,simulation}
mkdir -p tests/{core,db,gui,api,simulation}
mkdir -p docs/{api,user,dev}
mkdir -p resources
mkdir -p scripts
mkdir -p build

# Move header files to include directory
mv *.hpp include/ 2>/dev/null
mv core/*.hpp include/core/ 2>/dev/null
mv db/*.hpp include/db/ 2>/dev/null
mv gui/*.hpp include/gui/ 2>/dev/null
mv api/*.hpp include/api/ 2>/dev/null
mv simulation/*.hpp include/simulation/ 2>/dev/null

# Move source files to src directory
mv *.cpp src/ 2>/dev/null
mv core/*.cpp src/core/ 2>/dev/null
mv db/*.cpp src/db/ 2>/dev/null
mv gui/*.cpp src/gui/ 2>/dev/null
mv api/*.cpp src/api/ 2>/dev/null
mv simulation/*.cpp src/simulation/ 2>/dev/null

# Move test files
mv *_test.cpp tests/ 2>/dev/null
mv core/*_test.cpp tests/core/ 2>/dev/null
mv db/*_test.cpp tests/db/ 2>/dev/null
mv gui/*_test.cpp tests/gui/ 2>/dev/null
mv api/*_test.cpp tests/api/ 2>/dev/null
mv simulation/*_test.cpp tests/simulation/ 2>/dev/null

# Create basic documentation structure
echo "# API Documentation" > docs/api/README.md
echo "# User Manual" > docs/user/README.md
echo "# Developer Guide" > docs/dev/README.md

# Create basic test structure
for dir in tests/*; do
    if [ -d "$dir" ]; then
        echo "add_subdirectory($(basename $dir))" >> tests/CMakeLists.txt
    fi
done

# Set permissions
chmod +x scripts/*.sh

echo "Project structure organized successfully!"
