#include "gui/MainWindow.hpp"
#include <QMenuBar>
#include <QStatusBar>
#include <QMessageBox>
#include <QFileDialog>
#include <spdlog/spdlog.h>

namespace reqdb {
namespace gui {

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent) {
    setupUi();
    createMenuBar();
    setupStatusBar();
}

void MainWindow::setupUi() {
    setWindowTitle(tr("Employee Survey System"));
    resize(1200, 800);
}

void MainWindow::createMenuBar() {
    auto* menuBar = new QMenuBar(this);
    setMenuBar(menuBar);

    // File Menu
    auto* fileMenu = menuBar->addMenu(tr("&File"));
    
    auto* newAction = new QAction(tr("&New Project"), this);
    newAction->setShortcut(QKeySequence::New);
    fileMenu->addAction(newAction);
    connect(newAction, &QAction::triggered, this, &MainWindow::newProject);

    auto* openAction = new QAction(tr("&Open Project"), this);
    openAction->setShortcut(QKeySequence::Open);
    fileMenu->addAction(openAction);
    connect(openAction, &QAction::triggered, this, &MainWindow::openProject);

    fileMenu->addSeparator();

    auto* exitAction = new QAction(tr("E&xit"), this);
    exitAction->setShortcut(QKeySequence::Quit);
    fileMenu->addAction(exitAction);
    connect(exitAction, &QAction::triggered, this, &QWidget::close);
}

void MainWindow::setupStatusBar() {
    auto* statusBar = new QStatusBar(this);
    setStatusBar(statusBar);
    statusBar->showMessage(tr("Ready"));
}

void MainWindow::newProject() {
    QMessageBox::information(this, tr("New Project"), 
                           tr("Create new project functionality coming soon!"));
}

void MainWindow::openProject() {
    QString fileName = QFileDialog::getOpenFileName(this,
        tr("Open Project"), QString(),
        tr("Project Files (*.json);;All Files (*)"));

    if (!fileName.isEmpty()) {
        QMessageBox::information(this, tr("Open Project"), 
                               tr("Opening project: %1").arg(fileName));
    }
}

} // namespace gui
} // namespace reqdb
