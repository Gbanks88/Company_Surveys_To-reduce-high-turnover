#pragma once

#include <string>
#include <vector>
#include <memory>
#include <chrono>
#include <nlohmann/json.hpp>
#include "core/User.hpp"

namespace reqdb {
namespace core {

/**
 * @brief Represents a project in the requirements management system
 */
class Project {
public:
    /**
     * @brief Creates a new project
     * @param title The project title
     * @param description The project description
     * @param owner The project owner
     */
    Project(std::string title, std::string description, std::shared_ptr<User> owner);

    /**
     * @brief Get the project title
     * @return The project title
     */
    const std::string& getTitle() const { return title_; }

    /**
     * @brief Get the project description
     * @return The project description
     */
    const std::string& getDescription() const { return description_; }

    /**
     * @brief Get the project owner
     * @return Shared pointer to the project owner
     */
    std::shared_ptr<User> getOwner() const { return owner_; }

    /**
     * @brief Get the project creation date
     * @return The creation date
     */
    std::chrono::system_clock::time_point getCreatedAt() const { return createdAt_; }

    /**
     * @brief Add a collaborator to the project
     * @param user The user to add as a collaborator
     * @return True if the user was added, false if they were already a collaborator
     */
    bool addCollaborator(std::shared_ptr<User> user);

    /**
     * @brief Remove a collaborator from the project
     * @param username The username of the collaborator to remove
     * @return True if the user was removed, false if they weren't a collaborator
     */
    bool removeCollaborator(const std::string& username);

    /**
     * @brief Check if a user is a collaborator on the project
     * @param username The username to check
     * @return True if the user is a collaborator, false otherwise
     */
    bool isCollaborator(const std::string& username) const;

    /**
     * @brief Convert the project to JSON format
     * @return JSON object representing the project
     */
    nlohmann::json toJson() const;

    /**
     * @brief Create a project from JSON format
     * @param json JSON object representing the project
     * @param userLookup Function to look up users by username
     * @return Unique pointer to the created project
     */
    static std::unique_ptr<Project> fromJson(
        const nlohmann::json& json,
        const std::function<std::shared_ptr<User>(const std::string&)>& userLookup);

private:
    std::string title_;
    std::string description_;
    std::shared_ptr<User> owner_;
    std::vector<std::shared_ptr<User>> collaborators_;
    std::chrono::system_clock::time_point createdAt_;
};

} // namespace core
} // namespace reqdb
