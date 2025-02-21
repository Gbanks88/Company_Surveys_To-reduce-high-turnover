#pragma once

#include <string>
#include <nlohmann/json.hpp>

namespace Core {

class User {
public:
    User(const std::string& id, const std::string& name, 
         const std::string& email, const std::string& role);

    bool verifyPassword(const std::string& password) const;

    // Getters
    std::string getId() const;
    std::string getName() const;
    std::string getEmail() const;
    std::string getRole() const;

    // Setters
    void setName(const std::string& name);
    void setEmail(const std::string& email);
    void setRole(const std::string& role);

    // Serialization
    nlohmann::json toJson() const;
    void fromJson(const nlohmann::json& j);

private:
    std::string id_;
    std::string name_;
    std::string email_;
    std::string role_;
};

} // namespace Core
