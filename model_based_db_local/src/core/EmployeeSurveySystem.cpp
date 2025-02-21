#include "EmployeeSurveySystem.hpp"
#include <random>
#include <algorithm>
#include <ctime>

namespace Core {

SurveyQuestion::SurveyQuestion(const std::string& question, Category category, 
                             Frequency frequency, int weight)
    : question_(question), category_(category), 
      frequency_(frequency), weight_(weight) {}

EmployeeSurvey::EmployeeSurvey(const std::shared_ptr<User>& employee, 
                             SurveyQuestion::Frequency frequency)
    : employee_(employee), frequency_(frequency),
      createdAt_(std::chrono::system_clock::now()) {}

void EmployeeSurvey::addQuestion(const SurveyQuestion& question) {
    questions_[question.getQuestion()] = question;
}

void EmployeeSurvey::submitResponse(const std::string& questionId, 
                                  const Response& response) {
    responses_[questionId] = response;
    if (responses_.size() == questions_.size()) {
        completedAt_ = std::chrono::system_clock::now();
    }
}

bool EmployeeSurvey::isCompleted() const {
    return responses_.size() == questions_.size();
}

EmployeeSurveySystem::EmployeeSurveySystem() {
    // Initialize question bank with default questions
    initializeQuestionBank();
}

std::shared_ptr<EmployeeSurvey> EmployeeSurveySystem::generateWeeklySurvey(
    const std::shared_ptr<User>& employee) {
    auto survey = std::make_shared<EmployeeSurvey>(employee, 
                                                 SurveyQuestion::Frequency::Weekly);
    
    auto questions = selectQuestionsForSurvey(employee, SurveyQuestion::Frequency::Weekly);
    questions = personalizeQuestions(employee, questions);
    
    for (const auto& question : questions) {
        survey->addQuestion(question);
    }
    
    employeeSurveyHistory_[employee->getId()].push_back(survey);
    return survey;
}

std::vector<SurveyQuestion> EmployeeSurveySystem::selectQuestionsForSurvey(
    const std::shared_ptr<User>& employee,
    SurveyQuestion::Frequency frequency) const {
    std::vector<SurveyQuestion> selectedQuestions;
    
    // Get employee interests and project objectives
    auto interests = analyzeEmployeeInterests(employee);
    
    // Select questions based on frequency and interests
    for (const auto& [category, questions] : questionBank_) {
        if (interests[category] > 0.7) {  // High interest areas
            auto categoryQuestions = questions;
            std::shuffle(categoryQuestions.begin(), categoryQuestions.end(), 
                        std::mt19937(std::random_device()()));
            
            // Select more questions from high-interest categories
            size_t numQuestions = (frequency == SurveyQuestion::Frequency::Weekly) ? 2 :
                                (frequency == SurveyQuestion::Frequency::Quarterly) ? 4 : 6;
            
            for (size_t i = 0; i < std::min(numQuestions, categoryQuestions.size()); ++i) {
                selectedQuestions.push_back(categoryQuestions[i]);
            }
        }
    }
    
    return selectedQuestions;
}

std::vector<SurveyQuestion> EmployeeSurveySystem::personalizeQuestions(
    const std::shared_ptr<User>& employee,
    const std::vector<SurveyQuestion>& baseQuestions) const {
    std::vector<SurveyQuestion> personalizedQuestions;
    
    for (const auto& question : baseQuestions) {
        // Add context based on employee's role and projects
        std::string personalizedQuestion = question.getQuestion();
        personalizedQuestion = personalizedQuestion.replace(
            personalizedQuestion.find("{ROLE}"),
            5,
            employee->getRole()
        );
        
        // Create new question with personalized content
        personalizedQuestions.emplace_back(
            personalizedQuestion,
            question.getCategory(),
            question.getFrequency(),
            question.getWeight()
        );
    }
    
    return personalizedQuestions;
}

double EmployeeSurveySystem::calculateRetentionScore(
    const std::shared_ptr<User>& employee) const {
    double score = 0.0;
    int totalWeight = 0;
    
    // Get recent surveys
    const auto& surveys = employeeSurveyHistory_.at(employee->getId());
    if (surveys.empty()) return 0.0;
    
    // Calculate weighted average of recent responses
    for (const auto& survey : surveys) {
        for (const auto& [questionId, response] : survey->getResponses()) {
            const auto& question = survey->getQuestion(questionId);
            score += response.rating * question.getWeight();
            totalWeight += question.getWeight();
        }
    }
    
    return totalWeight > 0 ? score / totalWeight : 0.0;
}

EmployeeSurveySystem::RetentionReport 
EmployeeSurveySystem::generateRetentionReport(
    const std::shared_ptr<User>& employee) const {
    RetentionReport report;
    
    // Calculate overall retention score
    report.overallScore = calculateRetentionScore(employee);
    
    // Calculate category scores
    for (const auto& [category, _] : questionBank_) {
        report.categoryScores[category] = calculateCategoryScore(employee, category);
    }
    
    // Identify risk factors
    report.riskFactors = identifyRiskFactors(report.categoryScores);
    
    // Generate recommendations
    report.recommendations = suggestCareerGrowthOpportunities(employee);
    
    return report;
}

void EmployeeSurveySystem::initializeQuestionBank() {
    // Weekly questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with your current project assignments?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Weekly
    ));
    
    // Quarterly questions
    addQuestionToBank(SurveyQuestion(
        "How well does your current role align with your career goals?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly
    ));
    
    // Yearly questions
    addQuestionToBank(SurveyQuestion(
        "How do you see your long-term career progression at the company?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Yearly
    ));
    
    // Add more questions for each category and frequency...
}

} // namespace Core
