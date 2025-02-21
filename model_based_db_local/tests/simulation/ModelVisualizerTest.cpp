#include <gtest/gtest.h>
#include <QApplication>
#include "simulation/ModelVisualizer.hpp"

using namespace reqdb::simulation;

TEST(ModelVisualizerTest, Creation) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    ModelVisualizer visualizer;
    EXPECT_TRUE(visualizer.isEnabled());
}

TEST(ModelVisualizerTest, ViewportSetup) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    ModelVisualizer visualizer;
    EXPECT_TRUE(visualizer.viewport() != nullptr);
}
