#include "EmployeeSurveySystem.hpp"

namespace Core {

void EmployeeSurveySystem::initializeRoleSpecificQuestions() {
    // Software Engineer Questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with the technical challenges in your current projects?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Weekly,
        "software_engineer"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your satisfaction with the code review process:",
        SurveyQuestion::Category::TeamDynamics,
        SurveyQuestion::Frequency::Weekly,
        "software_engineer"
    ));

    addQuestionToBank(SurveyQuestion(
        "How well does our tech stack align with your career goals?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly,
        "software_engineer"
    ));

    // Project Manager Questions
    addQuestionToBank(SurveyQuestion(
        "How effectively is your team meeting sprint goals?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Weekly,
        "project_manager"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate the effectiveness of current project tracking tools:",
        SurveyQuestion::Category::WorkEnvironment,
        SurveyQuestion::Frequency::Quarterly,
        "project_manager"
    ));

    // Systems Engineer Questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with the current system architecture?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Quarterly,
        "systems_engineer"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your ability to influence architectural decisions:",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly,
        "systems_engineer"
    ));

    // DevOps Engineer Questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with our CI/CD processes?",
        SurveyQuestion::Category::WorkEnvironment,
        SurveyQuestion::Frequency::Weekly,
        "devops_engineer"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate the effectiveness of our monitoring solutions:",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Quarterly,
        "devops_engineer"
    ));

    // Technical Lead Questions
    addQuestionToBank(SurveyQuestion(
        "How effectively can you mentor team members?",
        SurveyQuestion::Category::Mentorship,
        SurveyQuestion::Frequency::Weekly,
        "tech_lead"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your ability to influence technical decisions:",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly,
        "tech_lead"
    ));

    // Department Manager Questions
    addQuestionToBank(SurveyQuestion(
        "How effectively are you able to develop your team members?",
        SurveyQuestion::Category::Mentorship,
        SurveyQuestion::Frequency::Weekly,
        "department_manager"
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your satisfaction with department resource allocation:",
        SurveyQuestion::Category::CompanyDirection,
        SurveyQuestion::Frequency::Quarterly,
        "department_manager"
    ));
}

} // namespace Core
