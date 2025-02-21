#pragma once

#include <QMainWindow>
#include <QMenuBar>
#include <QToolBar>
#include <QDockWidget>
#include <QStatusBar>
#include <QTabWidget>
#include "db/DatabaseManager.hpp"
#include "gui/ProjectView.hpp"
#include "gui/RequirementEditor.hpp"
#include "gui/DiagramEditor.hpp"
#include "gui/UIComponents.hpp"

namespace eco {
namespace gui {

class DashboardWidget;
class RequirementsWidget;
class MetricsWidget;

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit MainWindow(db::DatabaseManager* dbManager, QWidget* parent = nullptr);
    ~MainWindow() override = default;

private:
    void setupUI();
    void createMenus();
    void createToolbar();
    void createDockWidgets();
    void createCentralWidget();
    void setupConnections();
    void setupTheme();
    void showWelcomeScreen();

    // UI Elements
    QMenuBar* menuBar_;
    QToolBar* mainToolBar_;
    QStatusBar* statusBar_;
    QDockWidget* projectDock_;
    QDockWidget* propertiesDock_;
    QTabWidget* centralTabs_;
    ProjectView* projectView_;
    RequirementEditor* requirementEditor_;
    DiagramEditor* diagramEditor_;

    // Welcome screen widgets
    QWidget* welcomeWidget_;
    void createWelcomeWidget();
    void addRecentProjects();
    void addQuickStartGuide();

    db::DatabaseManager* dbManager_;

private slots:
    void onNewProject();
    void onOpenProject();
    void onSaveProject();
    void onProjectSelected(const QString& projectId);
    void onRequirementCreated();
    void onDiagramCreated();
    void onShowHelp();
    void onShowTutorial();
    void onShowAbout();
};

} // namespace gui
} // namespace eco
