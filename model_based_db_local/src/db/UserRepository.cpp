#include "db/UserRepository.hpp"
#include <spdlog/spdlog.h>
#include <sqlite3.h>

namespace reqdb {
namespace db {

UserRepository::UserRepository(sqlite3* db) : db_(db) {}

bool UserRepository::createUser(const core::User& user) {
    const char* sql = R"(
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?);
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    // Bind parameters
    sqlite3_bind_text(stmt, 1, user.getUsername().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, user.getEmail().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, user.getPasswordHash().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 4, static_cast<int>(user.getRole()));
    
    rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    
    if (rc != SQLITE_DONE) {
        spdlog::error("Failed to execute statement: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    return true;
}

std::optional<core::User> UserRepository::findByUsername(const std::string& username) {
    const char* sql = R"(
        SELECT username, email, password_hash, role
        FROM users
        WHERE username = ?;
    )";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        spdlog::error("Failed to prepare statement: {}", sqlite3_errmsg(db_));
        return std::nullopt;
    }
    
    sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_STATIC);
    
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        core::User user;
        user.setUsername(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0)));
        user.setEmail(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        user.setPasswordHash(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
        user.setRole(static_cast<core::User::Role>(sqlite3_column_int(stmt, 3)));
        
        sqlite3_finalize(stmt);
        return user;
    }
    
    sqlite3_finalize(stmt);
    return std::nullopt;
}

} // namespace db
} // namespace reqdb
