add_executable(gui_tests
    MainWindowTest.cpp
    DiagramEditorTest.cpp
    RequirementEditorTest.cpp
    ProjectViewTest.cpp
)

target_link_libraries(gui_tests PRIVATE
    reqdb_gui
    GTest::gtest_main
)

add_test(NAME gui_tests COMMAND gui_tests)
