#include <gtest/gtest.h>
#include "db/ProjectRepository.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::db;

TEST(ProjectRepositoryTest, CreateProject) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    ProjectRepository repo(&dbManager);
    auto project = repo.createProject("Test Project", "Test Description");
    EXPECT_TRUE(project != nullptr);
    EXPECT_EQ(project->getName(), "Test Project");
}

TEST(ProjectRepositoryTest, GetProject) {
    DatabaseManager dbManager(":memory:");
    dbManager.initialize();
    
    ProjectRepository repo(&dbManager);
    auto project = repo.createProject("Test Project", "Test Description");
    EXPECT_TRUE(project != nullptr);
    
    auto retrieved = repo.getProject(project->getId());
    EXPECT_TRUE(retrieved != nullptr);
    EXPECT_EQ(retrieved->getName(), project->getName());
}
