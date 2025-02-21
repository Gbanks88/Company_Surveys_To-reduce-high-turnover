add_executable(api_tests
    RESTServerTest.cpp
    WebSocketServerTest.cpp
    APIHandlersTest.cpp
)

target_link_libraries(api_tests PRIVATE
    reqdb_api
    GTest::gtest_main
)

add_test(NAME api_tests COMMAND api_tests)
