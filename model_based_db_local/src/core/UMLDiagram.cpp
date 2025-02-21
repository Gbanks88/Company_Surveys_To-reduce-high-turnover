#include "core/UMLDiagram.hpp"
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

UMLDiagram::UMLDiagram(const std::string& name, DiagramType type)
    : name_(name), type_(type) {}

void UMLDiagram::setName(const std::string& name) {
    name_ = name;
}

void UMLDiagram::setContent(const std::string& content) {
    content_ = content;
}

std::string UMLDiagram::getName() const {
    return name_;
}

std::string UMLDiagram::getContent() const {
    return content_;
}

UMLDiagram::DiagramType UMLDiagram::getType() const {
    return type_;
}

nlohmann::json UMLDiagram::toJson() const {
    nlohmann::json j;
    j["name"] = name_;
    j["type"] = static_cast<int>(type_);
    j["content"] = content_;
    j["created_at"] = created_at_;
    j["updated_at"] = updated_at_;
    return j;
}

void UMLDiagram::fromJson(const nlohmann::json& j) {
    name_ = j["name"];
    type_ = static_cast<DiagramType>(j["type"].get<int>());
    content_ = j["content"];
    created_at_ = j["created_at"];
    updated_at_ = j["updated_at"];
}

} // namespace core
} // namespace reqdb
