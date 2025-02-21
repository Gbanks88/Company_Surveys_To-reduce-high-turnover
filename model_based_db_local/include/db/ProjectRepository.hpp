#pragma once

#include "core/Project.hpp"
#include <optional>
#include <string>

struct sqlite3;

namespace reqdb {
namespace db {

class ProjectRepository {
public:
    explicit ProjectRepository(sqlite3* db);

    bool createProject(const core::Project& project);
    std::optional<core::Project> findById(const std::string& id);

private:
    sqlite3* db_;
};

} // namespace db
} // namespace reqdb
