#pragma once

#include <string>
#include <vector>
#include <memory>
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

/**
 * @brief Represents a user in the system with authentication and authorization capabilities
 */
class User {
public:
    enum class Role {
        ADMIN,
        PROJECT_MANAGER,
        DEVELOPER,
        VIEWER
    };

    /**
     * @brief Creates a new user
     * @param username The unique username
     * @param email The user's email address
     * @param role The user's role in the system
     */
    User(std::string username, std::string email, Role role);

    /**
     * @brief Get the user's unique username
     * @return The username
     */
    const std::string& getUsername() const { return username_; }

    /**
     * @brief Get the user's email address
     * @return The email address
     */
    const std::string& getEmail() const { return email_; }

    /**
     * @brief Get the user's role
     * @return The user's role
     */
    Role getRole() const { return role_; }

    /**
     * @brief Set the user's password hash
     * @param hash The bcrypt hash of the password
     */
    void setPasswordHash(const std::string& hash) { passwordHash_ = hash; }

    /**
     * @brief Verify if the provided password matches the stored hash
     * @param password The password to verify
     * @return True if the password matches, false otherwise
     */
    bool verifyPassword(const std::string& password) const;

    /**
     * @brief Convert the user to JSON format
     * @return JSON object representing the user
     */
    nlohmann::json toJson() const;

    /**
     * @brief Create a user from JSON format
     * @param json JSON object representing the user
     * @return Unique pointer to the created user
     */
    static std::unique_ptr<User> fromJson(const nlohmann::json& json);

private:
    std::string username_;
    std::string email_;
    std::string passwordHash_;
    Role role_;
};

} // namespace core
} // namespace reqdb
