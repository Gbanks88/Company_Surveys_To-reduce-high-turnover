#pragma once

#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTabWidget>
#include <QLabel>
#include <QPushButton>
#include <QListWidget>
#include <QGroupBox>
#include <QCheckBox>
#include <QStatusBar>
#include <QProgressBar>
#include <QTableWidget>
#include <memory>
#include "../core/EmployeeSurveySystem.hpp"
#include "../db/SurveyDatabase.hpp"

namespace GUI {

class SurveyMainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit SurveyMainWindow(QWidget* parent = nullptr);

private slots:
    void onSurveySelected();
    void onNotificationSettingChanged();
    void onExportData();
    void onGenerateReport();

private:
    // UI Setup
    void setupUI();
    void setupHeader();
    void setupDashboardTab();
    void setupSurveyTab();
    void setupAnalyticsTab();
    void setupSettingsTab();
    void setupSummaryCard(const QString& title, const QString& icon, QHBoxLayout* layout);
    void setupConnections();
    
    // Data loading
    void loadUserData();
    void updateAnalytics();

    // Core components
    std::shared_ptr<Core::EmployeeSurveySystem> surveySystem_;
    std::shared_ptr<DB::SurveyDatabase> database_;

    // Main UI components
    QVBoxLayout* mainLayout_;
    QTabWidget* tabWidget_;
    QStatusBar* statusBar_;

    // Header components
    QLabel* userInfo_;

    // Dashboard components
    QListWidget* activityList_;
    QProgressBar* weeklyProgress_;
    QProgressBar* quarterlyProgress_;
    QProgressBar* yearlyProgress_;

    // Survey components
    QListWidget* surveyListWidget_;
    QWidget* surveyForm_;

    // Analytics components
    QTableWidget* retentionTable_;
    QTableWidget* satisfactionTable_;
    QTableWidget* growthTable_;

    // Settings components
    QCheckBox* emailNotifications_;
    QCheckBox* slackNotifications_;
    QCheckBox* mobileNotifications_;
};

} // namespace GUI
