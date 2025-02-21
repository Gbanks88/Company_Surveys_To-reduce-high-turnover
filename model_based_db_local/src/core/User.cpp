#include "User.hpp"
#include <spdlog/spdlog.h>
#include <fmt/format.h>

namespace Core {

User::User(const std::string& id, const std::string& name, 
          const std::string& email, const std::string& role)
    : id_(id), name_(name), email_(email), role_(role) {}

bool User::verifyPassword(const std::string& password) const {
    // TODO: Implement proper password verification
    (void)password;  // Silence unused parameter warning
    return true;
}

std::string User::getId() const { return id_; }
std::string User::getName() const { return name_; }
std::string User::getEmail() const { return email_; }
std::string User::getRole() const { return role_; }

void User::setName(const std::string& name) { name_ = name; }
void User::setEmail(const std::string& email) { email_ = email; }
void User::setRole(const std::string& role) { role_ = role; }

nlohmann::json User::toJson() const {
    return {
        {"id", id_},
        {"name", name_},
        {"email", email_},
        {"role", role_}
    };
}

void User::fromJson(const nlohmann::json& j) {
    try {
        id_ = j.at("id").get<std::string>();
        name_ = j.at("name").get<std::string>();
        email_ = j.at("email").get<std::string>();
        role_ = j.at("role").get<std::string>();
    } catch (const std::exception& e) {
        spdlog::error(fmt::format("Failed to parse user JSON: {}", e.what()));
        throw;
    }
}

} // namespace Core
