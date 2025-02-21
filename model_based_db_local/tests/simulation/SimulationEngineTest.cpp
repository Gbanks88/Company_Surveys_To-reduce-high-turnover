#include <gtest/gtest.h>
#include "simulation/SimulationEngine.hpp"

using namespace reqdb::simulation;

TEST(SimulationEngineTest, Initialization) {
    SimulationEngine engine;
    EXPECT_TRUE(engine.initialize());
}

TEST(SimulationEngineTest, BasicSimulation) {
    SimulationEngine engine;
    EXPECT_TRUE(engine.initialize());
    EXPECT_TRUE(engine.start());
    EXPECT_TRUE(engine.stop());
}
