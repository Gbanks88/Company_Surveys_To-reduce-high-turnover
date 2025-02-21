#include <gtest/gtest.h>
#include "db/RequirementRepository.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::db;

TEST(RequirementRepositoryTest, CreateRequirement) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    RequirementRepository repo(&dbManager);
    auto req = repo.createRequirement("Test Requirement", "Test Description");
    EXPECT_TRUE(req != nullptr);
    EXPECT_EQ(req->getTitle(), "Test Requirement");
}

TEST(RequirementRepositoryTest, GetRequirement) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    RequirementRepository repo(&dbManager);
    auto req = repo.createRequirement("Test Requirement", "Test Description");
    EXPECT_TRUE(req != nullptr);
    
    auto retrieved = repo.getRequirement(req->getId());
    EXPECT_TRUE(retrieved != nullptr);
    EXPECT_EQ(retrieved->getTitle(), req->getTitle());
}
