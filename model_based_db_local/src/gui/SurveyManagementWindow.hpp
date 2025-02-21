#pragma once

#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QTabWidget>
#include <QPushButton>
#include <QLabel>
#include <QComboBox>
#include <QSpinBox>
#include <QTextEdit>
#include <QCalendarWidget>
#include <QProgressBar>
#include <QChart>
#include <QChartView>
#include <memory>
#include "../core/EmployeeSurveySystem.hpp"
#include "../db/SurveyDatabase.hpp"

namespace GUI {

class SurveyManagementWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit SurveyManagementWindow(QWidget* parent = nullptr);
    ~SurveyManagementWindow() = default;

private slots:
    // Survey taking
    void startSurvey();
    void submitSurvey();
    void saveDraft();

    // Survey management
    void scheduleNewSurvey();
    void viewSurveyResults();
    void exportReport();

    // Analytics
    void updateRetentionChart();
    void updateInterestChart();
    void generateTeamReport();

private:
    // UI setup methods
    void setupUI();
    void createSurveyTab();
    void createManagementTab();
    void createAnalyticsTab();
    void createSchedulingTab();

    // UI components
    QTabWidget* tabWidget_;
    
    // Survey taking components
    QWidget* surveyTab_;
    QVBoxLayout* surveyLayout_;
    QLabel* surveyTitle_;
    QTextEdit* responseArea_;
    QPushButton* submitButton_;
    QPushButton* saveButton_;
    QProgressBar* progressBar_;

    // Survey management components
    QWidget* managementTab_;
    QComboBox* surveyTypeCombo_;
    QCalendarWidget* scheduleCalendar_;
    QPushButton* scheduleButton_;
    QPushButton* exportButton_;

    // Analytics components
    QWidget* analyticsTab_;
    QChartView* retentionChart_;
    QChartView* interestChart_;
    QComboBox* timeRangeCombo_;
    QPushButton* generateReportButton_;

    // Data members
    std::shared_ptr<Core::EmployeeSurveySystem> surveySystem_;
    std::shared_ptr<DB::SurveyDatabase> database_;
    std::shared_ptr<Core::EmployeeSurvey> currentSurvey_;

    // Helper methods
    void loadSurveyQuestions();
    void updateCharts();
    void scheduleNextSurvey();
    void showNotification(const QString& message);
};

} // namespace GUI
