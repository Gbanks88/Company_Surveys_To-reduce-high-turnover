#pragma once

#include <string>
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

class Traceability {
public:
    enum class RelationType {
        DEPENDS_ON,
        DERIVED_FROM,
        IMPLEMENTS,
        VERIFIES,
        REFINES,
        CONFLICTS_WITH
    };

    Traceability(const std::string& sourceId = "", const std::string& targetId = "", 
                RelationType type = RelationType::DEPENDS_ON);
    
    std::string getSourceId() const;
    std::string getTargetId() const;
    RelationType getType() const;
    
    nlohmann::json toJson() const;
    void fromJson(const nlohmann::json& j);

private:
    std::string sourceId_;
    std::string targetId_;
    RelationType type_;
    std::string created_at_;
    std::string updated_at_;
};

} // namespace core
} // namespace reqdb
