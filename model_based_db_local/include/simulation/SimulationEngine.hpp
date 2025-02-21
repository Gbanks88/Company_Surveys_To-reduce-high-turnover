#pragma once

namespace reqdb {
namespace simulation {

class SimulationEngine {
public:
    SimulationEngine();

    bool initialize();
    void update(float deltaTime);
    void render();
    void shutdown();
};

} // namespace simulation
} // namespace reqdb
