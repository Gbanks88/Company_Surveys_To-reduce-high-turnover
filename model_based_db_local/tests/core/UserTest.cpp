#include <gtest/gtest.h>
#include "core/User.hpp"

using namespace reqdb::core;

class UserTest : public ::testing::Test {
protected:
    void SetUp() override {
        user = std::make_unique<User>("testuser", "test@example.com", User::Role::DEVELOPER);
    }

    std::unique_ptr<User> user;
};

TEST_F(UserTest, ConstructorSetsBasicProperties) {
    EXPECT_EQ(user->getUsername(), "testuser");
    EXPECT_EQ(user->getEmail(), "test@example.com");
    EXPECT_EQ(user->getRole(), User::Role::DEVELOPER);
}

TEST_F(UserTest, PasswordVerification) {
    // Initially no password is set
    EXPECT_FALSE(user->verifyPassword("password123"));

    // Set a password hash
    user->setPasswordHash("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYQNB8UHUYzPT");
    
    // Test password verification (Note: actual verification is not implemented yet)
    EXPECT_FALSE(user->verifyPassword("wrongpassword"));
}

TEST_F(UserTest, JsonSerialization) {
    nlohmann::json j = user->toJson();
    
    EXPECT_EQ(j["username"], "testuser");
    EXPECT_EQ(j["email"], "test@example.com");
    EXPECT_EQ(j["role"], static_cast<int>(User::Role::DEVELOPER));
}

TEST_F(UserTest, JsonDeserialization) {
    nlohmann::json j = {
        {"username", "newuser"},
        {"email", "new@example.com"},
        {"role", static_cast<int>(User::Role::ADMIN)},
        {"password_hash", "somehash"}
    };

    auto newUser = User::fromJson(j);
    ASSERT_NE(newUser, nullptr);
    EXPECT_EQ(newUser->getUsername(), "newuser");
    EXPECT_EQ(newUser->getEmail(), "new@example.com");
    EXPECT_EQ(newUser->getRole(), User::Role::ADMIN);
}

TEST_F(UserTest, InvalidJsonDeserialization) {
    nlohmann::json j = {
        {"username", "newuser"}
        // Missing required fields
    };

    auto newUser = User::fromJson(j);
    EXPECT_EQ(newUser, nullptr);
}
