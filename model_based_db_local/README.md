# Model-Based Requirements Management System

A comprehensive C++ framework for managing project requirements with advanced testing and integration capabilities.

## Features

- Modern C++17 implementation
- Qt6-based GUI with rich requirement editing
- UML diagram integration
- Real-time collaboration via WebSocket
- REST API for external integrations
- SQLite database for persistent storage
- Traceability management
- Advanced simulation capabilities
- Geospatial integration
- Role-based access control

## Dependencies

- CMake 3.15+
- C++17 compliant compiler
- Qt6 (Core, Widgets, WebEngineWidgets)
- Boost 1.81.0
- SQLite3 3.45.0
- OpenSSL 3.1.0
- nlohmann_json 3.11.2
- spdlog 1.11.0
- GTest 1.14.0 (for testing)

## Building

```bash
# Create build directory
mkdir build && cd build

# Configure with CMake
cmake ..

# Build
cmake --build .

# Run tests
ctest
```

## Project Structure

```
.
├── CMakeLists.txt
├── include/
│   ├── core/
│   │   ├── User.hpp
│   │   ├── Project.hpp
│   │   ├── Requirement.hpp
│   │   ├── UMLDiagram.hpp
│   │   └── Traceability.hpp
│   ├── db/
│   │   ├── DatabaseManager.hpp
│   │   ├── UserRepository.hpp
│   │   ├── ProjectRepository.hpp
│   │   └── RequirementRepository.hpp
│   ├── gui/
│   │   ├── MainWindow.hpp
│   │   ├── DiagramEditor.hpp
│   │   ├── RequirementEditor.hpp
│   │   └── ProjectView.hpp
│   ├── api/
│   │   ├── RESTServer.hpp
│   │   ├── WebSocketServer.hpp
│   │   └── APIHandlers.hpp
│   └── simulation/
│       ├── SimulationEngine.hpp
│       ├── ModelVisualizer.hpp
│       └── GeospatialIntegration.hpp
├── src/
│   └── [Implementation files]
├── tests/
│   └── [Test files]
└── README.md
```

## Usage

1. GUI Mode (Default):
```bash
./reqdb_app
```

2. Server-only Mode (for CI/CD integration):
```bash
./reqdb_app --server-only
```

## API Documentation

The system exposes both REST and WebSocket APIs for external integration:

- REST API (Port 8080):
  - GET /api/v1/requirements
  - POST /api/v1/requirements
  - GET /api/v1/projects
  - POST /api/v1/projects

- WebSocket API (Port 8081):
  - Real-time updates
  - Collaborative editing
  - Live simulation data

## Security

- Role-based access control
- Password hashing with bcrypt
- SSL/TLS encryption
- Input validation
- Audit logging
- Data protection

## License

MIT License
