#pragma once

#include <string>
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

class Requirement {
public:
    Requirement(const std::string& title = "", const std::string& description = "");
    
    void setTitle(const std::string& title);
    void setDescription(const std::string& description);
    
    std::string getTitle() const;
    std::string getDescription() const;
    
    nlohmann::json toJson() const;
    void fromJson(const nlohmann::json& j);

private:
    std::string title_;
    std::string description_;
    std::string created_at_;
    std::string updated_at_;
    std::string status_;
    int priority_;
    std::string assignee_;
};

} // namespace core
} // namespace reqdb
