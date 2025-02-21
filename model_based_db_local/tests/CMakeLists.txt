find_package(GTest REQUIRED)

# Enable CTest integration
include(GoogleTest)

# Add test subdirectories
add_subdirectory(api)
add_subdirectory(core)
add_subdirectory(db)
add_subdirectory(gui)
add_subdirectory(simulation)
