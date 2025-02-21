#include <gtest/gtest.h>
#include "core/Project.hpp"

using namespace reqdb::core;

class ProjectTest : public ::testing::Test {
protected:
    void SetUp() override {
        owner = std::make_shared<User>("owner", "owner@example.com", User::Role::PROJECT_MANAGER);
        project = std::make_unique<Project>("Test Project", "A test project", owner);
        
        collaborator1 = std::make_shared<User>("user1", "user1@example.com", User::Role::DEVELOPER);
        collaborator2 = std::make_shared<User>("user2", "user2@example.com", User::Role::DEVELOPER);
    }

    std::shared_ptr<User> owner;
    std::unique_ptr<Project> project;
    std::shared_ptr<User> collaborator1;
    std::shared_ptr<User> collaborator2;
};

TEST_F(ProjectTest, ConstructorSetsBasicProperties) {
    EXPECT_EQ(project->getTitle(), "Test Project");
    EXPECT_EQ(project->getDescription(), "A test project");
    EXPECT_EQ(project->getOwner(), owner);
    EXPECT_NE(project->getCreatedAt(), std::chrono::system_clock::time_point());
}

TEST_F(ProjectTest, AddCollaborator) {
    EXPECT_TRUE(project->addCollaborator(collaborator1));
    EXPECT_TRUE(project->isCollaborator(collaborator1->getUsername()));
    
    // Adding same collaborator twice should fail
    EXPECT_FALSE(project->addCollaborator(collaborator1));
    
    // Adding owner as collaborator should fail
    EXPECT_FALSE(project->addCollaborator(owner));
    
    // Adding null collaborator should fail
    EXPECT_FALSE(project->addCollaborator(nullptr));
}

TEST_F(ProjectTest, RemoveCollaborator) {
    EXPECT_TRUE(project->addCollaborator(collaborator1));
    EXPECT_TRUE(project->addCollaborator(collaborator2));
    
    EXPECT_TRUE(project->removeCollaborator(collaborator1->getUsername()));
    EXPECT_FALSE(project->isCollaborator(collaborator1->getUsername()));
    EXPECT_TRUE(project->isCollaborator(collaborator2->getUsername()));
    
    // Removing non-existent collaborator should fail
    EXPECT_FALSE(project->removeCollaborator("nonexistent"));
}

TEST_F(ProjectTest, JsonSerialization) {
    project->addCollaborator(collaborator1);
    project->addCollaborator(collaborator2);
    
    nlohmann::json j = project->toJson();
    
    EXPECT_EQ(j["title"], "Test Project");
    EXPECT_EQ(j["description"], "A test project");
    EXPECT_EQ(j["owner"], "owner");
    EXPECT_EQ(j["collaborators"].size(), 2);
    EXPECT_EQ(j["collaborators"][0], "user1");
    EXPECT_EQ(j["collaborators"][1], "user2");
}

TEST_F(ProjectTest, JsonDeserialization) {
    auto userLookup = [this](const std::string& username) -> std::shared_ptr<User> {
        if (username == "owner") return owner;
        if (username == "user1") return collaborator1;
        if (username == "user2") return collaborator2;
        return nullptr;
    };

    nlohmann::json j = {
        {"title", "New Project"},
        {"description", "A new project"},
        {"owner", "owner"},
        {"created_at", std::chrono::system_clock::to_time_t(std::chrono::system_clock::now())},
        {"collaborators", {"user1", "user2"}}
    };

    auto newProject = Project::fromJson(j, userLookup);
    ASSERT_NE(newProject, nullptr);
    EXPECT_EQ(newProject->getTitle(), "New Project");
    EXPECT_EQ(newProject->getDescription(), "A new project");
    EXPECT_EQ(newProject->getOwner(), owner);
    EXPECT_TRUE(newProject->isCollaborator("user1"));
    EXPECT_TRUE(newProject->isCollaborator("user2"));
}

TEST_F(ProjectTest, InvalidJsonDeserialization) {
    auto userLookup = [](const std::string&) { return nullptr; };

    nlohmann::json j = {
        {"title", "New Project"}
        // Missing required fields
    };

    auto newProject = Project::fromJson(j, userLookup);
    EXPECT_EQ(newProject, nullptr);
}
