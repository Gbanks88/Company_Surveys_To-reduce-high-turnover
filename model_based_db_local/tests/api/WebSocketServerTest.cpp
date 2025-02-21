#include <gtest/gtest.h>
#include "api/WebSocketServer.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::api;
using namespace reqdb::db;

TEST(WebSocketServerTest, ServerInitialization) {
    DatabaseManager dbManager(":memory:");
    WebSocketServer server(8081, &dbManager);
    EXPECT_TRUE(server.initialize());
}

TEST(WebSocketServerTest, StartStop) {
    DatabaseManager dbManager(":memory:");
    WebSocketServer server(8081, &dbManager);
    EXPECT_TRUE(server.start());
    EXPECT_TRUE(server.stop());
}
