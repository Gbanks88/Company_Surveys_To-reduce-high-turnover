# Core library
add_library(reqdb_core
    core/User.cpp
    core/Project.cpp
    core/Requirement.cpp
    core/UMLDiagram.cpp
    core/Traceability.cpp
)

target_include_directories(reqdb_core PUBLIC
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(reqdb_core PUBLIC
    Qt6::Core
    Boost::system
    Boost::filesystem
    nlohmann_json::nlohmann_json
    OpenSSL::SSL
    OpenSSL::Crypto
    SQLite::SQLite3
    spdlog::spdlog
)

# GUI library
add_library(reqdb_gui
    gui/MainWindow.cpp
    gui/DiagramEditor.cpp
    gui/RequirementEditor.cpp
    gui/ProjectView.cpp
    gui/SurveyMainWindow.cpp
)

target_link_libraries(reqdb_gui PUBLIC
    reqdb_core
    Qt6::Widgets
    Qt6::Sql
)

# Database library
add_library(reqdb_db
    db/DatabaseManager.cpp
    db/UserRepository.cpp
    db/ProjectRepository.cpp
    db/RequirementRepository.cpp
)

target_link_libraries(reqdb_db PUBLIC
    reqdb_core
)

# API library
add_library(reqdb_api
    api/RESTServer.cpp
    api/APIHandlers.cpp
    api/WebSocketServer.cpp
)

target_link_libraries(reqdb_api PUBLIC
    reqdb_core
    reqdb_db
)

# Simulation library
add_library(reqdb_simulation
    simulation/SimulationEngine.cpp
    simulation/ModelVisualizer.cpp
    simulation/GeospatialIntegration.cpp
)

target_link_libraries(reqdb_simulation PUBLIC
    reqdb_core
    reqdb_gui
)

# Main executable
add_executable(reqdb_app
    main.cpp
)

target_link_libraries(reqdb_app PRIVATE
    reqdb_core
    reqdb_gui
    reqdb_db
    reqdb_api
    reqdb_simulation
)

# Install rules
install(TARGETS reqdb_core reqdb_gui reqdb_db reqdb_api reqdb_simulation
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib/static
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/core/
    DESTINATION include/eco/core
    FILES_MATCHING PATTERN "*.hpp"
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/gui/
    DESTINATION include/eco/gui
    FILES_MATCHING PATTERN "*.hpp"
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/db/
    DESTINATION include/eco/db
    FILES_MATCHING PATTERN "*.hpp"
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/api/
    DESTINATION include/eco/api
    FILES_MATCHING PATTERN "*.hpp"
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/simulation/
    DESTINATION include/eco/simulation
    FILES_MATCHING PATTERN "*.hpp"
)
