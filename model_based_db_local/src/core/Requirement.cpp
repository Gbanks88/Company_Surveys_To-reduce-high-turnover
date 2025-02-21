#include "core/Requirement.hpp"
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

Requirement::Requirement(const std::string& title, const std::string& description)
    : title_(title), description_(description) {}

void Requirement::setTitle(const std::string& title) {
    title_ = title;
}

void Requirement::setDescription(const std::string& description) {
    description_ = description;
}

std::string Requirement::getTitle() const {
    return title_;
}

std::string Requirement::getDescription() const {
    return description_;
}

nlohmann::json Requirement::toJson() const {
    nlohmann::json j;
    j["title"] = title_;
    j["description"] = description_;
    j["created_at"] = created_at_;
    j["updated_at"] = updated_at_;
    j["status"] = status_;
    j["priority"] = priority_;
    j["assignee"] = assignee_;
    return j;
}

void Requirement::fromJson(const nlohmann::json& j) {
    title_ = j["title"];
    description_ = j["description"];
    created_at_ = j["created_at"];
    updated_at_ = j["updated_at"];
    status_ = j["status"];
    priority_ = j["priority"];
    assignee_ = j["assignee"];
}

} // namespace core
} // namespace reqdb
