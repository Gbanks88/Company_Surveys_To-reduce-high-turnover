#pragma once

#include <string>
#include <vector>
#include <memory>
#include <nlohmann/json.hpp>

namespace eco {
namespace core {

class Department;
class Employee;

class CompanyStructure {
public:
    static CompanyStructure& getInstance() {
        static CompanyStructure instance;
        return instance;
    }

    // Department management
    std::shared_ptr<Department> addDepartment(const std::string& name, const std::string& description);
    void removeDepartment(const std::string& name);
    std::shared_ptr<Department> getDepartment(const std::string& name);
    std::vector<std::shared_ptr<Department>> getAllDepartments() const;

    // Employee management
    std::shared_ptr<Employee> addEmployee(const std::string& name, const std::string& role,
                                        const std::string& departmentName);
    void removeEmployee(const std::string& id);
    std::shared_ptr<Employee> getEmployee(const std::string& id);
    std::vector<std::shared_ptr<Employee>> getAllEmployees() const;

    // Survey and metrics
    void conductSurvey(const std::string& surveyName);
    nlohmann::json getSurveyResults(const std::string& surveyName) const;
    void generateMetrics();
    nlohmann::json getMetrics() const;

    // Import/Export
    void importFromJson(const std::string& jsonPath);
    void exportToJson(const std::string& jsonPath) const;
    
    // Database operations
    void saveToDatabase();
    void loadFromDatabase();

private:
    CompanyStructure() = default;
    ~CompanyStructure() = default;
    CompanyStructure(const CompanyStructure&) = delete;
    CompanyStructure& operator=(const CompanyStructure&) = delete;

    std::vector<std::shared_ptr<Department>> departments_;
    std::vector<std::shared_ptr<Employee>> employees_;
    nlohmann::json metrics_;
    nlohmann::json surveyResults_;
};

class Department {
public:
    Department(const std::string& name, const std::string& description);

    // Getters and setters
    std::string getName() const { return name_; }
    std::string getDescription() const { return description_; }
    void setDescription(const std::string& description) { description_ = description; }

    // Employee management
    void addEmployee(std::shared_ptr<Employee> employee);
    void removeEmployee(const std::string& employeeId);
    std::vector<std::shared_ptr<Employee>> getEmployees() const;

    // Metrics
    nlohmann::json getMetrics() const;
    void updateMetrics();

private:
    std::string name_;
    std::string description_;
    std::vector<std::shared_ptr<Employee>> employees_;
    nlohmann::json metrics_;
};

class Employee {
public:
    Employee(const std::string& name, const std::string& role, const std::string& departmentName);

    // Getters and setters
    std::string getId() const { return id_; }
    std::string getName() const { return name_; }
    std::string getRole() const { return role_; }
    std::string getDepartmentName() const { return departmentName_; }

    void setRole(const std::string& role) { role_ = role; }
    void setDepartmentName(const std::string& departmentName) { departmentName_ = departmentName; }

    // Survey participation
    void participateInSurvey(const std::string& surveyName, const nlohmann::json& responses);
    nlohmann::json getSurveyResponses(const std::string& surveyName) const;

private:
    std::string id_;
    std::string name_;
    std::string role_;
    std::string departmentName_;
    nlohmann::json surveyResponses_;
};

} // namespace core
} // namespace eco
