#pragma once

#include <string>
#include <vector>
#include <map>
#include <memory>
#include "EmployeeSurveySystem.hpp"

namespace Core {

class ReportExporter {
public:
    enum class ReportType {
        IndividualSurvey,
        TeamSummary,
        DepartmentAnalytics,
        RetentionAnalysis,
        CareerGrowthTracking,
        SkillGapAnalysis,
        CompanyWideTrends
    };

    enum class ExportFormat {
        PDF,
        Excel,
        HTML,
        JSON,
        CSV
    };

    struct ReportConfig {
        ReportType type;
        ExportFormat format;
        std::string timeRange;
        std::vector<std::string> includedMetrics;
        bool includeCharts;
        bool includeRawData;
        std::map<std::string, std::string> customParams;
    };

    ReportExporter(std::shared_ptr<EmployeeSurveySystem> surveySystem);

    // Report generation
    std::string generateReport(const ReportConfig& config);
    std::string generateIndividualReport(const std::string& userId);
    std::string generateTeamReport(const std::string& teamId);
    std::string generateDepartmentReport(const std::string& departmentId);

    // Custom report building
    void addMetric(const std::string& metricName,
                  const std::function<double(const std::string&)>& calculator);
    void addChartGenerator(const std::string& chartName,
                          const std::function<std::string(const std::string&)>& generator);

    // Template management
    void setReportTemplate(ReportType type, const std::string& templateContent);
    std::string getReportTemplate(ReportType type) const;

    // Export helpers
    void exportToPDF(const std::string& reportContent, const std::string& outputPath);
    void exportToExcel(const std::string& reportContent, const std::string& outputPath);
    void exportToHTML(const std::string& reportContent, const std::string& outputPath);

private:
    std::shared_ptr<EmployeeSurveySystem> surveySystem_;
    std::map<ReportType, std::string> reportTemplates_;
    std::map<std::string, std::function<double(const std::string&)>> metricCalculators_;
    std::map<std::string, std::function<std::string(const std::string&)>> chartGenerators_;

    // Report generation helpers
    std::string processTemplate(const std::string& templateContent,
                              const std::map<std::string, std::string>& data);
    std::string generateCharts(const ReportConfig& config);
    std::string formatData(const std::vector<std::map<std::string, std::string>>& data,
                          ExportFormat format);

    // Data processing helpers
    std::vector<std::map<std::string, std::string>> gatherMetrics(
        const std::string& targetId,
        const ReportConfig& config);
    std::map<std::string, double> calculateTrends(
        const std::string& targetId,
        const std::string& timeRange);
};

} // namespace Core
