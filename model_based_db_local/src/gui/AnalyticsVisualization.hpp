#pragma once

#include <QWidget>
#include <QChartView>
#include <QLineSeries>
#include <QBarSet>
#include <QBarSeries>
#include <QPieSeries>
#include <QDateTimeAxis>
#include <QValueAxis>
#include <QGridLayout>
#include <QComboBox>
#include <QPushButton>
#include <memory>
#include "../core/EmployeeSurveySystem.hpp"

namespace GUI {

class AnalyticsVisualization : public QWidget {
    Q_OBJECT

public:
    explicit AnalyticsVisualization(
        std::shared_ptr<Core::EmployeeSurveySystem> surveySystem,
        QWidget* parent = nullptr);

    // Chart creation
    void createRetentionTrendChart();
    void createCategoryScoresChart();
    void createTeamSatisfactionChart();
    void createCareerGrowthChart();
    void createSkillGapAnalysisChart();

public slots:
    void updateCharts();
    void exportCharts();
    void filterByDepartment(const QString& department);
    void filterByTimeRange(const QString& range);

private:
    // UI Components
    QGridLayout* mainLayout_;
    QChartView* retentionChart_;
    QChartView* categoryScoresChart_;
    QChartView* teamSatisfactionChart_;
    QChartView* careerGrowthChart_;
    QChartView* skillGapChart_;
    
    QComboBox* departmentFilter_;
    QComboBox* timeRangeFilter_;
    QPushButton* exportButton_;
    QPushButton* printButton_;

    // Data members
    std::shared_ptr<Core::EmployeeSurveySystem> surveySystem_;
    QString currentDepartment_;
    QString currentTimeRange_;

    // Chart creation helpers
    QChart* createTrendChart(const QString& title);
    QChart* createBarChart(const QString& title);
    QChart* createPieChart(const QString& title);
    
    // Data processing helpers
    void processRetentionData(QLineSeries* series);
    void processCategoryScores(QBarSeries* series);
    void processTeamSatisfaction(QPieSeries* series);
    void processCareerGrowth(QLineSeries* series);
    void processSkillGaps(QBarSeries* series);

    // Export helpers
    void exportToPDF();
    void exportToExcel();
    void generateReport();
};

} // namespace GUI
