#pragma once

#include <string>
#include <vector>
#include <map>
#include <chrono>
#include <memory>
#include "EmployeeSurveySystem.hpp"

namespace Core {

class SurveyScheduler {
public:
    struct ScheduleConfig {
        bool enableWeekly;
        bool enableQuarterly;
        bool enableYearly;
        int weeklyDay;  // 0 = Sunday, 6 = Saturday
        int quarterlyMonth;  // Month within quarter (0-2)
        int yearlyMonth;  // Month within year (0-11)
        std::string timezone;
    };

    struct ScheduledSurvey {
        std::string employeeId;
        SurveyQuestion::Frequency frequency;
        std::chrono::system_clock::time_point scheduledTime;
        bool completed;
    };

    SurveyScheduler(std::shared_ptr<EmployeeSurveySystem> surveySystem);

    // Configuration
    void setScheduleConfig(const ScheduleConfig& config);
    ScheduleConfig getScheduleConfig() const;

    // Scheduling
    void scheduleAllSurveys();
    void scheduleSurveysForEmployee(const std::string& employeeId);
    void rescheduleMissedSurveys();

    // Survey management
    std::vector<ScheduledSurvey> getPendingSurveys() const;
    std::vector<ScheduledSurvey> getCompletedSurveys() const;
    void markSurveyComplete(const std::string& surveyId);

    // Notifications
    struct Notification {
        std::string employeeId;
        std::string message;
        std::chrono::system_clock::time_point sendTime;
        bool sent;
    };

    void scheduleReminders();
    std::vector<Notification> getPendingNotifications() const;
    void markNotificationSent(const std::string& notificationId);

private:
    std::shared_ptr<EmployeeSurveySystem> surveySystem_;
    ScheduleConfig config_;
    std::map<std::string, ScheduledSurvey> scheduledSurveys_;
    std::map<std::string, Notification> notifications_;

    // Helper methods
    std::chrono::system_clock::time_point calculateNextWeeklySurveyTime(
        const std::string& employeeId) const;
    std::chrono::system_clock::time_point calculateNextQuarterlySurveyTime(
        const std::string& employeeId) const;
    std::chrono::system_clock::time_point calculateNextYearlySurveyTime(
        const std::string& employeeId) const;

    void createRemindersForSurvey(const ScheduledSurvey& survey);
    bool isWorkingHours(const std::chrono::system_clock::time_point& time) const;
    void adjustForTimezone(std::chrono::system_clock::time_point& time) const;
};

} // namespace Core
