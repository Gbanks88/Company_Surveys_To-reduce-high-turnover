#include "db/DatabaseManager.hpp"
#include <spdlog/spdlog.h>
#include <sqlite3.h>

namespace reqdb {
namespace db {

DatabaseManager::DatabaseManager() {}

DatabaseManager::~DatabaseManager() {
    if (db_) {
        sqlite3_close(db_);
    }
}

bool DatabaseManager::initialize(const std::string& dbPath) {
    int rc = sqlite3_open(dbPath.c_str(), &db_);
    if (rc) {
        spdlog::error("Can't open database: {}", sqlite3_errmsg(db_));
        return false;
    }
    
    if (!createTables()) {
        spdlog::error("Failed to create database tables");
        return false;
    }
    
    return true;
}

bool DatabaseManager::createTables() {
    const char* sql = R"(
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            priority INTEGER,
            assignee TEXT
        );
        
        CREATE TABLE IF NOT EXISTS uml_diagrams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            type TEXT NOT NULL,
            FOREIGN KEY(source_id) REFERENCES requirements(id),
            FOREIGN KEY(target_id) REFERENCES requirements(id)
        );
    )";
    
    char* errMsg = nullptr;
    int rc = sqlite3_exec(db_, sql, nullptr, nullptr, &errMsg);
    
    if (rc != SQLITE_OK) {
        spdlog::error("SQL error: {}", errMsg);
        sqlite3_free(errMsg);
        return false;
    }
    
    return true;
}

} // namespace db
} // namespace reqdb
