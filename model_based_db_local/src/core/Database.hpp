#pragma once

#include <string>
#include <memory>
#include <vector>
#include <sqlite3.h>
#include <nlohmann/json.hpp>

namespace eco {
namespace core {

class Database {
public:
    Database(const std::string& dbPath);
    ~Database();

    // Initialize database schema
    bool initializeSchema();

    // Model operations
    bool createModel(const nlohmann::json& modelData);
    std::vector<nlohmann::json> getModels();
    bool updateModel(int modelId, const nlohmann::json& modelData);
    bool deleteModel(int modelId);

    // Requirement operations
    bool createRequirement(const nlohmann::json& reqData);
    std::vector<nlohmann::json> getRequirements(int modelId = -1);
    bool updateRequirement(int reqId, const nlohmann::json& reqData);
    bool deleteRequirement(int reqId);

    // Component operations
    bool createComponent(const nlohmann::json& compData);
    std::vector<nlohmann::json> getComponents(int modelId = -1);
    bool updateComponent(int compId, const nlohmann::json& compData);
    bool deleteComponent(int compId);

private:
    std::string dbPath_;
    sqlite3* db_;
    
    bool executeQuery(const std::string& query);
    std::vector<nlohmann::json> executeSelect(const std::string& query);
    void handleError(const std::string& operation);
};

} // namespace core
} // namespace eco
