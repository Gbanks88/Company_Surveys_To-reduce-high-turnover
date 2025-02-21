#include "core/Traceability.hpp"
#include <nlohmann/json.hpp>

namespace reqdb {
namespace core {

Traceability::Traceability(const std::string& sourceId, const std::string& targetId, RelationType type)
    : sourceId_(sourceId), targetId_(targetId), type_(type) {}

std::string Traceability::getSourceId() const {
    return sourceId_;
}

std::string Traceability::getTargetId() const {
    return targetId_;
}

Traceability::RelationType Traceability::getType() const {
    return type_;
}

nlohmann::json Traceability::toJson() const {
    nlohmann::json j;
    j["source_id"] = sourceId_;
    j["target_id"] = targetId_;
    j["type"] = static_cast<int>(type_);
    j["created_at"] = created_at_;
    j["updated_at"] = updated_at_;
    return j;
}

void Traceability::fromJson(const nlohmann::json& j) {
    sourceId_ = j["source_id"];
    targetId_ = j["target_id"];
    type_ = static_cast<RelationType>(j["type"].get<int>());
    created_at_ = j["created_at"];
    updated_at_ = j["updated_at"];
}

} // namespace core
} // namespace reqdb
