#include "db/ProjectRepository.hpp"
#include <spdlog/spdlog.h>
#include <sqlite3.h>

namespace reqdb {
namespace db {

ProjectRepository::ProjectRepository(sqlite3* db) : db_(db) {}

bool ProjectRepository::createProject(const core::Project& project) {
    const char* sql = R"(
        INSERT INTO projects (title, description, owner_id)
        VALUES (?, ?, ?);
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    // Bind parameters
    sqlite3_bind_text(stmt, 1, project.getTitle().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, project.getDescription().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, project.getOwnerId().c_str(), -1, SQLITE_STATIC);
    
    rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    
    if (rc != SQLITE_DONE) {
        spdlog::error("Failed to execute statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    return true;
}

std::optional<core::Project> ProjectRepository::findById(const std::string& id) {
    const char* sql = R"(
        SELECT title, description, owner_id, created_at, updated_at
        FROM projects
        WHERE id = ?;
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return std::nullopt;
    }
    
    sqlite3_bind_text(stmt, 1, id.c_str(), -1, SQLITE_STATIC);
    
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        core::Project project;
        project.setTitle(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0)));
        project.setDescription(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        project.setOwnerId(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
        // TODO: Set timestamps
        
        sqlite3_finalize(stmt);
        return project;
    }
    
    sqlite3_finalize(stmt);
    return std::nullopt;
}

} // namespace db
} // namespace reqdb
