#pragma once

#include <QWidget>
#include <QTreeView>
#include <QLineEdit>
#include <QTextEdit>
#include <QPushButton>
#include <QComboBox>
#include <memory>
#include "../core/SurveySystem.hpp"

namespace eco {
namespace gui {

class SurveyDesignerWidget : public QWidget {
    Q_OBJECT

public:
    explicit SurveyDesignerWidget(QWidget* parent = nullptr);
    ~SurveyDesignerWidget();

private slots:
    void createNewSurvey();
    void addQuestion();
    void removeQuestion();
    void saveSurvey();
    void loadSurvey();
    void previewSurvey();
    void exportSurvey();
    void handleQuestionTypeChanged(const QString& type);
    void handleSurveySelected(const QModelIndex& index);

private:
    void setupUi();
    void createConnections();
    void updateQuestionPanel();
    void clearForm();
    void loadSurveyList();

    // UI Components
    QTreeView* surveyListView_;
    QLineEdit* surveyNameEdit_;
    QTextEdit* surveyDescriptionEdit_;
    QComboBox* questionTypeCombo_;
    QTextEdit* questionTextEdit_;
    QWidget* optionsWidget_;
    QPushButton* addQuestionBtn_;
    QPushButton* removeQuestionBtn_;
    QPushButton* saveBtn_;
    QPushButton* exportBtn_;
    QPushButton* previewBtn_;

    // Data
    std::shared_ptr<core::Survey> currentSurvey_;
    std::shared_ptr<core::Question> currentQuestion_;
};

class QuestionPreviewWidget : public QWidget {
    Q_OBJECT

public:
    explicit QuestionPreviewWidget(const core::Question& question, QWidget* parent = nullptr);

private:
    void setupUi(const core::Question& question);
    void createMultipleChoiceUI(const std::vector<std::string>& options);
    void createSingleChoiceUI(const std::vector<std::string>& options);
    void createTextUI();
    void createRatingUI();
    void createYesNoUI();
};

class SurveyPreviewDialog : public QDialog {
    Q_OBJECT

public:
    explicit SurveyPreviewDialog(const core::Survey& survey, QWidget* parent = nullptr);

private:
    void setupUi(const core::Survey& survey);
    void createQuestionWidgets(const std::vector<std::shared_ptr<core::Question>>& questions);
};

} // namespace gui
} // namespace eco
