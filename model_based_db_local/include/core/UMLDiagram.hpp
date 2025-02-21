#pragma once

#include <string>
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

class UMLDiagram {
public:
    enum class DiagramType {
        CLASS,
        SEQUENCE,
        ACTIVITY,
        STATE,
        COMPONENT,
        DEPLOYMENT
    };

    UMLDiagram(const std::string& name = "", DiagramType type = DiagramType::CLASS);
    
    void setName(const std::string& name);
    void setContent(const std::string& content);
    
    std::string getName() const;
    std::string getContent() const;
    DiagramType getType() const;
    
    nlohmann::json toJson() const;
    void fromJson(const nlohmann::json& j);

private:
    std::string name_;
    DiagramType type_;
    std::string content_;
    std::string created_at_;
    std::string updated_at_;
};

} // namespace core
} // namespace reqdb
