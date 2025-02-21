#include <gtest/gtest.h>
#include "api/RESTServer.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::api;
using namespace reqdb::db;

TEST(RESTServerTest, ServerInitialization) {
    DatabaseManager dbManager(":memory:");
    RESTServer server(8080, &dbManager);
    EXPECT_TRUE(server.initialize());
}

TEST(RESTServerTest, StartStop) {
    DatabaseManager dbManager(":memory:");
    RESTServer server(8080, &dbManager);
    EXPECT_TRUE(server.start());
    EXPECT_TRUE(server.stop());
}
