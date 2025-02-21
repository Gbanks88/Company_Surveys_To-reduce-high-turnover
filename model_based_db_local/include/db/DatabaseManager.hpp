#pragma once

#include <string>

struct sqlite3;

namespace reqdb {
namespace db {

class DatabaseManager {
public:
    DatabaseManager();
    ~DatabaseManager();

    bool initialize(const std::string& dbPath);

private:
    bool createTables();
    
    sqlite3* db_ = nullptr;
};

} // namespace db
} // namespace reqdb
