#include "core/Project.hpp"
#include <algorithm>
#include <spdlog/spdlog.h>
#include <fmt/format.h>

namespace reqdb {
namespace core {

Project::Project(std::string title, std::string description, std::shared_ptr<User> owner)
    : title_(std::move(title))
    , description_(std::move(description))
    , owner_(std::move(owner))
    , createdAt_(std::chrono::system_clock::now()) {
}

bool Project::addCollaborator(std::shared_ptr<User> user) {
    if (!user) {
        spdlog::error("Attempted to add null user as collaborator");
        return false;
    }

    if (user->getUsername() == owner_->getUsername()) {
        spdlog::warn("Attempted to add project owner as collaborator");
        return false;
    }

    auto it = std::find_if(collaborators_.begin(), collaborators_.end(),
        [&](const auto& collaborator) {
            return collaborator->getUsername() == user->getUsername();
        });

    if (it != collaborators_.end()) {
        spdlog::info("User {} is already a collaborator", user->getUsername());
        return false;
    }

    collaborators_.push_back(std::move(user));
    return true;
}

bool Project::removeCollaborator(const std::string& username) {
    auto it = std::find_if(collaborators_.begin(), collaborators_.end(),
        [&](const auto& collaborator) {
            return collaborator->getUsername() == username;
        });

    if (it == collaborators_.end()) {
        spdlog::info("User {} is not a collaborator", username);
        return false;
    }

    collaborators_.erase(it);
    return true;
}

bool Project::isCollaborator(const std::string& username) const {
    if (owner_->getUsername() == username) {
        return true;
    }

    return std::any_of(collaborators_.begin(), collaborators_.end(),
        [&](const auto& collaborator) {
            return collaborator->getUsername() == username;
        });
}

nlohmann::json Project::toJson() const {
    nlohmann::json j = {
        {"title", title_},
        {"description", description_},
        {"owner", owner_->getUsername()},
        {"created_at", std::chrono::system_clock::to_time_t(createdAt_)},
        {"collaborators", nlohmann::json::array()}
    };

    for (const auto& collaborator : collaborators_) {
        j["collaborators"].push_back(collaborator->getUsername());
    }

    return j;
}

std::unique_ptr<Project> Project::fromJson(
    const nlohmann::json& json,
    const std::function<std::shared_ptr<User>(const std::string&)>& userLookup) {
    try {
        auto owner = userLookup(json["owner"].get<std::string>());
        if (!owner) {
            spdlog::error("Failed to find project owner");
            return nullptr;
        }

        auto project = std::make_unique<Project>(
            json["title"].get<std::string>(),
            json["description"].get<std::string>(),
            owner
        );

        // Set creation time
        project->createdAt_ = std::chrono::system_clock::from_time_t(
            json["created_at"].get<std::time_t>()
        );

        // Add collaborators
        for (const auto& username : json["collaborators"]) {
            auto collaborator = userLookup(username.get<std::string>());
            if (collaborator) {
                project->addCollaborator(collaborator);
            } else {
                spdlog::warn(fmt::format("Failed to find collaborator: {}", username.get<std::string>()));
            }
        }

        return project;
    } catch (const std::exception& e) {
        spdlog::error(fmt::format("Failed to create project from JSON: {}", e.what()));
        return nullptr;
    }
}

} // namespace core
} // namespace reqdb
