#include <gtest/gtest.h>
#include "api/APIHandlers.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::api;
using namespace reqdb::db;

TEST(APIHandlersTest, RequirementEndpoints) {
    DatabaseManager dbManager(":memory:");
    APIHandlers handlers(&dbManager);
    EXPECT_TRUE(handlers.initialize());
}

TEST(APIHandlersTest, ProjectEndpoints) {
    DatabaseManager dbManager(":memory:");
    APIHandlers handlers(&dbManager);
    EXPECT_TRUE(handlers.initialize());
    EXPECT_TRUE(handlers.setupProjectEndpoints());
}
