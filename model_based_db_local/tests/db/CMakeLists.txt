add_executable(db_tests
    DatabaseManagerTest.cpp
    UserRepositoryTest.cpp
    ProjectRepositoryTest.cpp
    RequirementRepositoryTest.cpp
)

target_link_libraries(db_tests PRIVATE
    reqdb_db
    GTest::gtest_main
)

add_test(NAME db_tests COMMAND db_tests)
