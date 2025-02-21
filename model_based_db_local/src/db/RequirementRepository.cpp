#include "db/RequirementRepository.hpp"
#include <spdlog/spdlog.h>
#include <sqlite3.h>

namespace reqdb {
namespace db {

RequirementRepository::RequirementRepository(sqlite3* db) : db_(db) {}

bool RequirementRepository::createRequirement(const core::Requirement& requirement) {
    const char* sql = R"(
        INSERT INTO requirements (title, description, status, priority, assignee)
        VALUES (?, ?, ?, ?, ?);
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    // Bind parameters
    sqlite3_bind_text(stmt, 1, requirement.getTitle().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, requirement.getDescription().c_str(), -1, SQLITE_STATIC);
    // TODO: Add status, priority, and assignee bindings
    
    rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    
    if (rc != SQLITE_DONE) {
        spdlog::error("Failed to execute statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    return true;
}

std::optional<core::Requirement> RequirementRepository::findById(const std::string& id) {
    const char* sql = R"(
        SELECT title, description, status, priority, assignee, created_at, updated_at
        FROM requirements
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
        core::Requirement requirement;
        requirement.setTitle(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0)));
        requirement.setDescription(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        // TODO: Set other fields
        
        sqlite3_finalize(stmt);
        return requirement;
    }
    
    sqlite3_finalize(stmt);
    return std::nullopt;
}

std::vector<core::Requirement> RequirementRepository::findByProject(const std::string& projectId) {
    const char* sql = R"(
        SELECT r.title, r.description, r.status, r.priority, r.assignee, r.created_at, r.updated_at
        FROM requirements r
        JOIN project_requirements pr ON r.id = pr.requirement_id
        WHERE pr.project_id = ?;
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return {};
    }
    
    sqlite3_bind_text(stmt, 1, projectId.c_str(), -1, SQLITE_STATIC);
    
    std::vector<core::Requirement> requirements;
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        core::Requirement requirement;
        requirement.setTitle(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0)));
        requirement.setDescription(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        // TODO: Set other fields
        requirements.push_back(requirement);
    }
    
    sqlite3_finalize(stmt);
    return requirements;
}

} // namespace db
} // namespace reqdb
