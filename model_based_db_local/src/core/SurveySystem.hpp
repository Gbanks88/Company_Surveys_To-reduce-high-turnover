#pragma once

#include <string>
#include <vector>
#include <memory>
#include <nlohmann/json.hpp>
#include <QObject>

namespace eco {
namespace core {

class Survey;
class Question;
class Response;

class SurveySystem : public QObject {
    Q_OBJECT

public:
    static SurveySystem& getInstance() {
        static SurveySystem instance;
        return instance;
    }

    // Survey management
    std::shared_ptr<Survey> createSurvey(const std::string& name, const std::string& description);
    void deleteSurvey(const std::string& surveyId);
    std::shared_ptr<Survey> getSurvey(const std::string& surveyId);
    std::vector<std::shared_ptr<Survey>> getAllSurveys() const;

    // Survey distribution
    void distributeSurvey(const std::string& surveyId, const std::vector<std::string>& employeeIds);
    void closeSurvey(const std::string& surveyId);

    // Results and analytics
    nlohmann::json getResults(const std::string& surveyId) const;
    nlohmann::json generateAnalytics(const std::string& surveyId) const;
    void exportResults(const std::string& surveyId, const std::string& format, const std::string& path);

signals:
    void surveyCreated(const QString& surveyId);
    void surveyDistributed(const QString& surveyId);
    void surveyCompleted(const QString& surveyId);
    void responseReceived(const QString& surveyId, const QString& employeeId);

private:
    SurveySystem() = default;
    ~SurveySystem() = default;
    SurveySystem(const SurveySystem&) = delete;
    SurveySystem& operator=(const SurveySystem&) = delete;

    std::vector<std::shared_ptr<Survey>> surveys_;
};

class Survey {
public:
    Survey(const std::string& name, const std::string& description);

    // Question management
    void addQuestion(const std::string& text, const std::string& type, 
                    const std::vector<std::string>& options = {});
    void removeQuestion(size_t index);
    std::vector<std::shared_ptr<Question>> getQuestions() const;

    // Response management
    void addResponse(const std::string& employeeId, const std::vector<std::string>& answers);
    std::vector<std::shared_ptr<Response>> getResponses() const;

    // Status management
    bool isActive() const { return active_; }
    void setActive(bool active) { active_ = active; }

    // Getters
    std::string getId() const { return id_; }
    std::string getName() const { return name_; }
    std::string getDescription() const { return description_; }
    
    // Analytics
    nlohmann::json calculateMetrics() const;
    std::string generateReport() const;

private:
    std::string id_;
    std::string name_;
    std::string description_;
    bool active_;
    std::vector<std::shared_ptr<Question>> questions_;
    std::vector<std::shared_ptr<Response>> responses_;
};

class Question {
public:
    enum class Type {
        MultipleChoice,
        SingleChoice,
        Text,
        Rating,
        YesNo
    };

    Question(const std::string& text, Type type, const std::vector<std::string>& options = {});

    // Getters
    std::string getText() const { return text_; }
    Type getType() const { return type_; }
    std::vector<std::string> getOptions() const { return options_; }

    // Validation
    bool isValidAnswer(const std::string& answer) const;

private:
    std::string text_;
    Type type_;
    std::vector<std::string> options_;
};

class Response {
public:
    Response(const std::string& employeeId, const std::vector<std::string>& answers);

    // Getters
    std::string getEmployeeId() const { return employeeId_; }
    std::vector<std::string> getAnswers() const { return answers_; }
    std::string getTimestamp() const { return timestamp_; }

private:
    std::string employeeId_;
    std::vector<std::string> answers_;
    std::string timestamp_;
};

} // namespace core
} // namespace eco
