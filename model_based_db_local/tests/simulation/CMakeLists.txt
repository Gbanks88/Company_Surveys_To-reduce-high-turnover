add_executable(simulation_tests
    SimulationEngineTest.cpp
    ModelVisualizerTest.cpp
    GeospatialIntegrationTest.cpp
)

target_link_libraries(simulation_tests PRIVATE
    reqdb_simulation
    GTest::gtest_main
)

add_test(NAME simulation_tests COMMAND simulation_tests)
