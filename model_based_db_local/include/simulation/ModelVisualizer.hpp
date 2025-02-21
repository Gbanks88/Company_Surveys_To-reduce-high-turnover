#pragma once

#include <string>

namespace reqdb {
namespace simulation {

struct Camera {
    // TODO: Add camera parameters
};

class ModelVisualizer {
public:
    ModelVisualizer();

    bool initialize();
    void update(float deltaTime);
    void render();
    void shutdown();

    void loadModel(const std::string& path);
    void setCamera(const Camera& camera);
};

} // namespace simulation
} // namespace reqdb
