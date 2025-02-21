#include "EmployeeSurveySystem.hpp"

namespace Core {

void EmployeeSurveySystem::initializeQuestionBank() {
    // Weekly Questions
    addQuestionToBank(SurveyQuestion(
        "How energized do you feel about your current project tasks?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Weekly
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your work-life balance this week:",
        SurveyQuestion::Category::WorkLifeBalance,
        SurveyQuestion::Frequency::Weekly
    ));

    addQuestionToBank(SurveyQuestion(
        "How well is your team collaborating this week?",
        SurveyQuestion::Category::TeamDynamics,
        SurveyQuestion::Frequency::Weekly
    ));

    // Quarterly Questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with your career progression in the last quarter?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate the effectiveness of your mentorship experiences this quarter:",
        SurveyQuestion::Category::Mentorship,
        SurveyQuestion::Frequency::Quarterly
    ));

    addQuestionToBank(SurveyQuestion(
        "How well do your current projects align with your career goals?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your satisfaction with learning opportunities this quarter:",
        SurveyQuestion::Category::SkillDevelopment,
        SurveyQuestion::Frequency::Quarterly
    ));

    // Yearly Questions
    addQuestionToBank(SurveyQuestion(
        "How well does your compensation align with your contributions?",
        SurveyQuestion::Category::Compensation,
        SurveyQuestion::Frequency::Yearly
    ));

    addQuestionToBank(SurveyQuestion(
        "Rate your confidence in the company's direction:",
        SurveyQuestion::Category::CompanyDirection,
        SurveyQuestion::Frequency::Yearly
    ));

    addQuestionToBank(SurveyQuestion(
        "How likely are you to recommend our company as a great place to work?",
        SurveyQuestion::Category::JobSatisfaction,
        SurveyQuestion::Frequency::Yearly
    ));

    // Project-specific questions
    addQuestionToBank(SurveyQuestion(
        "How challenging do you find your current project tasks?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Weekly
    ));

    // Skill development questions
    addQuestionToBank(SurveyQuestion(
        "What new skills would you like to develop in your current role?",
        SurveyQuestion::Category::SkillDevelopment,
        SurveyQuestion::Frequency::Quarterly
    ));

    // Career growth questions
    addQuestionToBank(SurveyQuestion(
        "How clear is your path to promotion?",
        SurveyQuestion::Category::CareerGrowth,
        SurveyQuestion::Frequency::Quarterly
    ));

    // Team dynamics questions
    addQuestionToBank(SurveyQuestion(
        "Rate the level of support you receive from your team:",
        SurveyQuestion::Category::TeamDynamics,
        SurveyQuestion::Frequency::Weekly
    ));

    // Work environment questions
    addQuestionToBank(SurveyQuestion(
        "How satisfied are you with your work environment?",
        SurveyQuestion::Category::WorkEnvironment,
        SurveyQuestion::Frequency::Quarterly
    ));

    // Project alignment questions
    addQuestionToBank(SurveyQuestion(
        "How well do your current projects utilize your strengths?",
        SurveyQuestion::Category::ProjectEngagement,
        SurveyQuestion::Frequency::Quarterly
    ));

    // Professional development questions
    addQuestionToBank(SurveyQuestion(
        "Rate the quality of professional development opportunities:",
        SurveyQuestion::Category::SkillDevelopment,
        SurveyQuestion::Frequency::Yearly
    ));

    // Work-life balance questions
    addQuestionToBank(SurveyQuestion(
        "How manageable is your current workload?",
        SurveyQuestion::Category::WorkLifeBalance,
        SurveyQuestion::Frequency::Weekly
    ));

    // Company culture questions
    addQuestionToBank(SurveyQuestion(
        "How well does the company culture align with your values?",
        SurveyQuestion::Category::CompanyDirection,
        SurveyQuestion::Frequency::Yearly
    ));
}

} // namespace Core
