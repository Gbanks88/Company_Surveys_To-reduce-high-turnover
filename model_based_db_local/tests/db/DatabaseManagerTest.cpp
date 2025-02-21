#include <gtest/gtest.h>
#include "db/DatabaseManager.hpp"

using namespace reqdb::db;

TEST(DatabaseManagerTest, Initialization) {
    DatabaseManager dbManager(":memory:");
    EXPECT_TRUE(dbManager.initialize());
}

TEST(DatabaseManagerTest, TableCreation) {
    DatabaseManager dbManager(":memory:");
    EXPECT_TRUE(dbManager.initialize());
    EXPECT_TRUE(dbManager.createTables());
}
