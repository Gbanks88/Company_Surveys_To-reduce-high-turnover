add_executable(core_tests
    UserTest.cpp
    ProjectTest.cpp
    RequirementTest.cpp
    UMLDiagramTest.cpp
    TraceabilityTest.cpp
)

target_link_libraries(core_tests PRIVATE
    reqdb_core
    GTest::gtest_main
)

add_test(NAME core_tests COMMAND core_tests)
