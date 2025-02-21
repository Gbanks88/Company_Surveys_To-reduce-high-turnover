#pragma once

#include <string>
#include <vector>
#include <memory>
#include <sqlite3.h>
#include "../core/EmployeeSurveySystem.hpp"

namespace DB {

class SurveyDatabase {
public:
    SurveyDatabase(const std::string& dbPath);
    ~SurveyDatabase();

    // Schema initialization
    bool initializeSchema();

    // Question bank operations
    bool addQuestion(const Core::SurveyQuestion& question);
    bool updateQuestion(const std::string& questionId, const Core::SurveyQuestion& question);
    bool deleteQuestion(const std::string& questionId);
    std::vector<Core::SurveyQuestion> getQuestions(Core::SurveyQuestion::Frequency frequency);

    // Survey operations
    bool saveSurvey(const std::shared_ptr<Core::EmployeeSurvey>& survey);
    bool updateSurveyResponses(const std::string& surveyId, 
                             const std::map<std::string, Core::EmployeeSurvey::Response>& responses);
    std::vector<std::shared_ptr<Core::EmployeeSurvey>> getEmployeeSurveys(
        const std::string& employeeId,
        Core::SurveyQuestion::Frequency frequency);

    // Analytics queries
    double getAverageRetentionScore(const std::string& employeeId);
    std::map<Core::SurveyQuestion::Category, double> getCategoryScores(
        const std::string& employeeId);
    std::vector<std::string> getEmployeeInterests(const std::string& employeeId);

private:
    sqlite3* db_;
    
    // Helper methods for database operations
    bool executeQuery(const std::string& query);
    bool prepareStatement(const std::string& query, sqlite3_stmt** stmt);
};

} // namespace DB
