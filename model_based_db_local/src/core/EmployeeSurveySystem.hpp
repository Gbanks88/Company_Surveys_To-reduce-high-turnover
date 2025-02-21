#pragma once

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <chrono>
#include "User.cpp"

namespace Core {

class SurveyQuestion {
public:
    enum class Category {
        JobSatisfaction,
        CareerGrowth,
        WorkLifeBalance,
        ProjectEngagement,
        TeamDynamics,
        CompanyDirection,
        SkillDevelopment,
        Mentorship,
        Compensation,
        WorkEnvironment
    };

    enum class Frequency {
        Weekly,
        Quarterly,
        Yearly
    };

    SurveyQuestion(const std::string& question, Category category, 
                  Frequency frequency, int weight = 1);

    std::string getQuestion() const { return question_; }
    Category getCategory() const { return category_; }
    Frequency getFrequency() const { return frequency_; }
    int getWeight() const { return weight_; }

private:
    std::string question_;
    Category category_;
    Frequency frequency_;
    int weight_;
};

class EmployeeSurvey {
public:
    struct Response {
        int rating;  // 1-5 scale
        std::string comment;
        std::chrono::system_clock::time_point timestamp;
    };

    EmployeeSurvey(const std::shared_ptr<User>& employee, 
                  SurveyQuestion::Frequency frequency);

    void addQuestion(const SurveyQuestion& question);
    void submitResponse(const std::string& questionId, const Response& response);
    std::map<std::string, Response> getResponses() const;
    bool isCompleted() const;
    
private:
    std::shared_ptr<User> employee_;
    SurveyQuestion::Frequency frequency_;
    std::map<std::string, SurveyQuestion> questions_;
    std::map<std::string, Response> responses_;
    std::chrono::system_clock::time_point createdAt_;
    std::chrono::system_clock::time_point completedAt_;
};

class EmployeeSurveySystem {
public:
    EmployeeSurveySystem();

    // Survey Generation
    std::shared_ptr<EmployeeSurvey> generateWeeklySurvey(const std::shared_ptr<User>& employee);
    std::shared_ptr<EmployeeSurvey> generateQuarterlySurvey(const std::shared_ptr<User>& employee);
    std::shared_ptr<EmployeeSurvey> generateYearlySurvey(const std::shared_ptr<User>& employee);

    // Question Bank Management
    void addQuestionToBank(const SurveyQuestion& question);
    void removeQuestionFromBank(const std::string& questionId);
    std::vector<SurveyQuestion> getQuestionsForCategory(SurveyQuestion::Category category) const;

    // Analysis
    double calculateRetentionScore(const std::shared_ptr<User>& employee) const;
    std::map<SurveyQuestion::Category, double> analyzeEmployeeInterests(const std::shared_ptr<User>& employee) const;
    std::vector<std::string> suggestCareerGrowthOpportunities(const std::shared_ptr<User>& employee) const;
    
    // Reporting
    struct RetentionReport {
        double overallScore;
        std::vector<std::string> riskFactors;
        std::vector<std::string> recommendations;
        std::map<SurveyQuestion::Category, double> categoryScores;
    };

    RetentionReport generateRetentionReport(const std::shared_ptr<User>& employee) const;
    std::vector<RetentionReport> generateTeamReport(const std::string& teamId) const;
    std::vector<RetentionReport> generateDepartmentReport(const std::string& departmentId) const;

private:
    // Question selection and generation helpers
    std::vector<SurveyQuestion> selectQuestionsForSurvey(
        const std::shared_ptr<User>& employee,
        SurveyQuestion::Frequency frequency) const;
    
    std::vector<SurveyQuestion> personalizeQuestions(
        const std::shared_ptr<User>& employee,
        const std::vector<SurveyQuestion>& baseQuestions) const;

    // Analysis helpers
    double calculateCategoryScore(
        const std::shared_ptr<User>& employee,
        SurveyQuestion::Category category) const;
        
    std::vector<std::string> identifyRiskFactors(
        const std::map<SurveyQuestion::Category, double>& scores) const;

    // Storage
    std::map<SurveyQuestion::Category, std::vector<SurveyQuestion>> questionBank_;
    std::map<std::string, std::vector<std::shared_ptr<EmployeeSurvey>>> employeeSurveyHistory_;
};

} // namespace Core
