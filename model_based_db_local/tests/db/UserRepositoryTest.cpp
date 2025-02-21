#include <gtest/gtest.h>
#include "db/UserRepository.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::db;

TEST(UserRepositoryTest, CreateUser) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    UserRepository repo(&dbManager);
    auto user = repo.createUser("test_user", "test_password", "user");
    EXPECT_TRUE(user != nullptr);
    EXPECT_EQ(user->getUsername(), "test_user");
}

TEST(UserRepositoryTest, GetUser) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    UserRepository repo(&dbManager);
    auto user = repo.createUser("test_user", "test_password", "user");
    EXPECT_TRUE(user != nullptr);
    
    auto retrieved = repo.getUser("test_user");
    EXPECT_TRUE(retrieved != nullptr);
    EXPECT_EQ(retrieved->getUsername(), user->getUsername());
}
