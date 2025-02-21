#pragma once

#include "core/User.hpp"
#include <optional>
#include <string>

struct sqlite3;

namespace reqdb {
namespace db {

class UserRepository {
public:
    explicit UserRepository(sqlite3* db);

    bool createUser(const core::User& user);
    std::optional<core::User> findByUsername(const std::string& username);

private:
    sqlite3* db_;
};

} // namespace db
} // namespace reqdb
