#pragma once

#include "core/Requirement.hpp"
#include <optional>
#include <string>
#include <vector>

struct sqlite3;

namespace reqdb {
namespace db {

class RequirementRepository {
public:
    explicit RequirementRepository(sqlite3* db);

    bool createRequirement(const core::Requirement& requirement);
    std::optional<core::Requirement> findById(const std::string& id);
    std::vector<core::Requirement> findByProject(const std::string& projectId);

private:
    sqlite3* db_;
};

} // namespace db
} // namespace reqdb
