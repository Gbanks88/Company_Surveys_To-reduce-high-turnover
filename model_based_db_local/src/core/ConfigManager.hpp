#pragma once

#include <string>
#include <nlohmann/json.hpp>
#include <filesystem>

namespace eco {
namespace core {

class ConfigManager {
public:
    static ConfigManager& getInstance() {
        static ConfigManager instance;
        return instance;
    }

    void loadConfig(const std::string& configPath);
    void saveConfig();

    // Database settings
    std::string getDatabasePath() const;
    void setDatabasePath(const std::string& path);

    // Server settings
    std::string getServerHost() const;
    unsigned short getServerPort() const;
    bool getServerDebugMode() const;

    // Vehicle production settings
    struct VehicleConfig {
        double range;           // miles
        double topSpeed;        // mph
        double acceleration;    // 0-60 mph time
        double batteryCapacity; // kWh
        double chargingRate;    // kW
        int cycleLife;         // cycles
    };
    VehicleConfig getVehicleConfig() const;
    void setVehicleConfig(const VehicleConfig& config);

    // Production metrics
    struct ProductionConfig {
        int dailyTarget;        // units
        double qualityThreshold; // percent
        int cycleTimeTarget;    // minutes
    };
    ProductionConfig getProductionConfig() const;
    void setProductionConfig(const ProductionConfig& config);

private:
    ConfigManager() = default;
    ~ConfigManager() = default;
    ConfigManager(const ConfigManager&) = delete;
    ConfigManager& operator=(const ConfigManager&) = delete;

    nlohmann::json config_;
    std::filesystem::path configPath_;
};

} // namespace core
} // namespace eco
