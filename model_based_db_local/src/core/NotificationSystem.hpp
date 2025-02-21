#pragma once

#include <string>
#include <vector>
#include <map>
#include <chrono>
#include <memory>
#include <queue>
#include "EmployeeSurveySystem.hpp"

namespace Core {

class NotificationSystem {
public:
    enum class NotificationType {
        SurveyDue,
        SurveyOverdue,
        TeamReport,
        RetentionAlert,
        CareerGrowthOpportunity,
        SkillDevelopmentSuggestion
    };

    struct Notification {
        std::string id;
        std::string userId;
        NotificationType type;
        std::string message;
        std::chrono::system_clock::time_point createdAt;
        std::chrono::system_clock::time_point scheduledFor;
        bool isRead;
        int priority;  // 1-5, 5 being highest
        std::map<std::string, std::string> metadata;
    };

    NotificationSystem(std::shared_ptr<EmployeeSurveySystem> surveySystem);

    // Notification creation
    void scheduleSurveyReminder(const std::string& userId, 
                              const std::string& surveyId,
                              std::chrono::system_clock::time_point dueDate);
                              
    void createRetentionAlert(const std::string& userId, 
                            double retentionScore,
                            const std::vector<std::string>& riskFactors);
                            
    void suggestCareerGrowth(const std::string& userId,
                            const std::vector<std::string>& opportunities);

    // Notification management
    std::vector<Notification> getPendingNotifications(const std::string& userId);
    std::vector<Notification> getUnreadNotifications(const std::string& userId);
    void markAsRead(const std::string& notificationId);
    void dismiss(const std::string& notificationId);

    // Channel management
    void setEmailNotifications(const std::string& userId, bool enabled);
    void setSlackNotifications(const std::string& userId, bool enabled);
    void setMobileNotifications(const std::string& userId, bool enabled);

    // Templates
    void addNotificationTemplate(NotificationType type, 
                               const std::string& template_content);
    std::string renderTemplate(NotificationType type,
                             const std::map<std::string, std::string>& params);

    // Delivery
    void processQueue();
    bool sendNotification(const Notification& notification);

private:
    std::shared_ptr<EmployeeSurveySystem> surveySystem_;
    std::map<std::string, std::vector<Notification>> userNotifications_;
    std::map<NotificationType, std::string> notificationTemplates_;
    std::priority_queue<Notification> notificationQueue_;
    
    // User preferences
    struct UserPreferences {
        bool emailEnabled;
        bool slackEnabled;
        bool mobileEnabled;
        std::string timezone;
        std::map<NotificationType, bool> typePreferences;
    };
    std::map<std::string, UserPreferences> userPreferences_;

    // Helper methods
    void queueNotification(const Notification& notification);
    bool isWorkingHours(const std::string& userId) const;
    void cleanupOldNotifications();
    std::string generateNotificationId();
};

} // namespace Core
