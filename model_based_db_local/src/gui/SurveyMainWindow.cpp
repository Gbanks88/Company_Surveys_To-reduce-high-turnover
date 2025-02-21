#include "SurveyManagementWindow.hpp"
#include <QApplication>
#include <QStyle>
#include <QDesktopWidget>
#include <QMessageBox>
#include <QFileDialog>
#include <QStandardPaths>

namespace GUI {

SurveyMainWindow::SurveyMainWindow(QWidget* parent)
    : QMainWindow(parent)
    , surveySystem_(std::make_shared<Core::EmployeeSurveySystem>())
    , database_(std::make_shared<DB::SurveyDatabase>("surveys.db")) {
    
    setupUI();
    setupConnections();
    loadUserData();
}

void SurveyMainWindow::setupUI() {
    // Set window properties
    setWindowTitle("Employee Survey System");
    resize(1200, 800);
    setStyleSheet("QMainWindow { background-color: #f0f0f0; }");

    // Create central widget and main layout
    QWidget* centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    mainLayout_ = new QVBoxLayout(centralWidget);
    mainLayout_->setSpacing(10);
    mainLayout_->setContentsMargins(20, 20, 20, 20);

    // Create header
    setupHeader();

    // Create tab widget
    tabWidget_ = new QTabWidget(this);
    tabWidget_->setStyleSheet(
        "QTabWidget::pane { border: 1px solid #cccccc; }"
        "QTabWidget::tab-bar { left: 5px; }"
        "QTabBar::tab { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f8f8, stop: 1 #e8e8e8);"
        "border: 1px solid #cccccc; padding: 8px 12px; margin-right: 2px; }"
        "QTabBar::tab:selected { background: #ffffff; }"
    );

    // Add tabs
    setupDashboardTab();
    setupSurveyTab();
    setupAnalyticsTab();
    setupSettingsTab();

    mainLayout_->addWidget(tabWidget_);

    // Create status bar
    statusBar_ = new QStatusBar(this);
    setStatusBar(statusBar_);
    statusBar_->showMessage("Ready");
}

void SurveyMainWindow::setupHeader() {
    QWidget* header = new QWidget(this);
    QHBoxLayout* headerLayout = new QHBoxLayout(header);

    // Logo
    QLabel* logo = new QLabel("📊", this);
    logo->setStyleSheet("font-size: 24px;");
    headerLayout->addWidget(logo);

    // Title
    QLabel* title = new QLabel("Employee Survey System", this);
    title->setStyleSheet("font-size: 20px; font-weight: bold;");
    headerLayout->addWidget(title);

    // User info
    userInfo_ = new QLabel(this);
    userInfo_->setStyleSheet("font-size: 14px;");
    headerLayout->addWidget(userInfo_, 0, Qt::AlignRight);

    mainLayout_->addWidget(header);
}

void SurveyMainWindow::setupDashboardTab() {
    QWidget* dashboard = new QWidget(this);
    QVBoxLayout* dashboardLayout = new QVBoxLayout(dashboard);

    // Summary cards
    QHBoxLayout* cardsLayout = new QHBoxLayout();
    setupSummaryCard("Pending Surveys", "🎯", cardsLayout);
    setupSummaryCard("Team Satisfaction", "😊", cardsLayout);
    setupSummaryCard("Career Growth", "📈", cardsLayout);
    dashboardLayout->addLayout(cardsLayout);

    // Recent activity
    QGroupBox* recentActivity = new QGroupBox("Recent Activity", this);
    QVBoxLayout* activityLayout = new QVBoxLayout(recentActivity);
    activityList_ = new QListWidget(this);
    activityLayout->addWidget(activityList_);
    dashboardLayout->addWidget(recentActivity);

    tabWidget_->addTab(dashboard, "Dashboard");
}

void SurveyMainWindow::setupSurveyTab() {
    QWidget* surveyWidget = new QWidget(this);
    QVBoxLayout* surveyLayout = new QVBoxLayout(surveyWidget);

    // Survey list
    QGroupBox* surveyList = new QGroupBox("Available Surveys", this);
    QVBoxLayout* listLayout = new QVBoxLayout(surveyList);
    surveyListWidget_ = new QListWidget(this);
    listLayout->addWidget(surveyListWidget_);
    surveyLayout->addWidget(surveyList);

    // Survey content
    QGroupBox* surveyContent = new QGroupBox("Survey", this);
    QVBoxLayout* contentLayout = new QVBoxLayout(surveyContent);
    surveyForm_ = new QWidget(this);
    contentLayout->addWidget(surveyForm_);
    surveyLayout->addWidget(surveyContent);

    tabWidget_->addTab(surveyWidget, "Surveys");
}

void SurveyMainWindow::setupAnalyticsTab() {
    analyticsWidget_ = new AnalyticsVisualization(surveySystem_, this);
    tabWidget_->addTab(analyticsWidget_, "Analytics");
}

void SurveyMainWindow::setupSettingsTab() {
    QWidget* settings = new QWidget(this);
    QVBoxLayout* settingsLayout = new QVBoxLayout(settings);

    // Notification settings
    QGroupBox* notifications = new QGroupBox("Notification Preferences", this);
    QVBoxLayout* notifyLayout = new QVBoxLayout(notifications);
    
    emailNotifications_ = new QCheckBox("Email Notifications", this);
    slackNotifications_ = new QCheckBox("Slack Notifications", this);
    mobileNotifications_ = new QCheckBox("Mobile Notifications", this);
    
    notifyLayout->addWidget(emailNotifications_);
    notifyLayout->addWidget(slackNotifications_);
    notifyLayout->addWidget(mobileNotifications_);
    
    settingsLayout->addWidget(notifications);

    tabWidget_->addTab(settings, "Settings");
}

void SurveyMainWindow::setupSummaryCard(const QString& title, 
                                      const QString& icon, 
                                      QHBoxLayout* layout) {
    QGroupBox* card = new QGroupBox(this);
    card->setStyleSheet(
        "QGroupBox { background-color: white; border-radius: 10px; "
        "padding: 15px; min-width: 200px; }"
    );
    
    QVBoxLayout* cardLayout = new QVBoxLayout(card);
    
    QLabel* iconLabel = new QLabel(icon, this);
    iconLabel->setStyleSheet("font-size: 24px;");
    cardLayout->addWidget(iconLabel, 0, Qt::AlignHCenter);
    
    QLabel* titleLabel = new QLabel(title, this);
    titleLabel->setStyleSheet("font-size: 16px; font-weight: bold;");
    cardLayout->addWidget(titleLabel, 0, Qt::AlignHCenter);
    
    QLabel* valueLabel = new QLabel("0", this);
    valueLabel->setStyleSheet("font-size: 24px; color: #2196F3;");
    cardLayout->addWidget(valueLabel, 0, Qt::AlignHCenter);
    
    layout->addWidget(card);
}

void SurveyMainWindow::setupConnections() {
    // Connect survey list selection
    connect(surveyListWidget_, &QListWidget::itemSelectionChanged,
            this, &SurveyMainWindow::onSurveySelected);

    // Connect notification toggles
    connect(emailNotifications_, &QCheckBox::toggled,
            this, &SurveyMainWindow::onNotificationSettingChanged);
    connect(slackNotifications_, &QCheckBox::toggled,
            this, &SurveyMainWindow::onNotificationSettingChanged);
    connect(mobileNotifications_, &QCheckBox::toggled,
            this, &SurveyMainWindow::onNotificationSettingChanged);
}

void SurveyMainWindow::loadUserData() {
    // TODO: Load actual user data
    userInfo_->setText("John Doe | Software Engineer");
    
    // Load available surveys
    surveyListWidget_->addItem("Weekly Engagement Survey");
    surveyListWidget_->addItem("Quarterly Career Development");
    surveyListWidget_->addItem("Annual Satisfaction Survey");
    
    // Load recent activity
    activityList_->addItem("Completed Weekly Survey - 2 days ago");
    activityList_->addItem("Career Growth Meeting - 1 week ago");
    activityList_->addItem("Team Feedback Session - 2 weeks ago");
}

void SurveyMainWindow::onSurveySelected() {
    QListWidgetItem* item = surveyListWidget_->currentItem();
    if (!item) return;
    
    // TODO: Load actual survey content
    statusBar_->showMessage("Loading survey: " + item->text());
}

void SurveyMainWindow::onNotificationSettingChanged() {
    // TODO: Save notification preferences
    statusBar_->showMessage("Notification settings updated");
}

} // namespace GUI
