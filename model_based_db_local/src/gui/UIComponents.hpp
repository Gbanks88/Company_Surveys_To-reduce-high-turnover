#pragma once

#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QComboBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QMessageBox>
#include <QToolTip>
#include <QStatusBar>
#include <QStyle>
#include <QApplication>

namespace reqdb::gui {

class StyledButton : public QPushButton {
    Q_OBJECT
public:
    explicit StyledButton(const QString& text, QWidget* parent = nullptr) 
        : QPushButton(text, parent) {
        setStyleSheet(
            "QPushButton {"
            "    background-color: #2196F3;"
            "    color: white;"
            "    border-radius: 4px;"
            "    padding: 6px 12px;"
            "    font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #1976D2;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #0D47A1;"
            "}"
        );
    }
};

class InfoLabel : public QLabel {
    Q_OBJECT
public:
    explicit InfoLabel(const QString& text, QWidget* parent = nullptr)
        : QLabel(text, parent) {
        setStyleSheet(
            "QLabel {"
            "    color: #424242;"
            "    font-size: 13px;"
            "    margin-bottom: 4px;"
            "}"
        );
    }
};

class StyledLineEdit : public QLineEdit {
    Q_OBJECT
public:
    explicit StyledLineEdit(QWidget* parent = nullptr)
        : QLineEdit(parent) {
        setStyleSheet(
            "QLineEdit {"
            "    border: 1px solid #BDBDBD;"
            "    border-radius: 4px;"
            "    padding: 6px;"
            "    background-color: white;"
            "    font-size: 13px;"
            "}"
            "QLineEdit:focus {"
            "    border: 2px solid #2196F3;"
            "}"
        );
    }
};

class GroupContainer : public QGroupBox {
    Q_OBJECT
public:
    explicit GroupContainer(const QString& title, QWidget* parent = nullptr)
        : QGroupBox(title, parent) {
        setStyleSheet(
            "QGroupBox {"
            "    background-color: #FFFFFF;"
            "    border: 1px solid #E0E0E0;"
            "    border-radius: 6px;"
            "    margin-top: 16px;"
            "    padding: 12px;"
            "    font-size: 14px;"
            "}"
            "QGroupBox::title {"
            "    color: #1976D2;"
            "    subcontrol-origin: margin;"
            "    left: 8px;"
            "    padding: 0 3px;"
            "}"
        );
    }
};

class HelpTooltip {
public:
    static void show(QWidget* widget, const QString& text) {
        QToolTip::setStyleSheet(
            "QToolTip {"
            "    background-color: #424242;"
            "    color: white;"
            "    border: none;"
            "    padding: 8px;"
            "    border-radius: 4px;"
            "    font-size: 12px;"
            "}"
        );
        widget->setToolTip(text);
    }
};

class StatusMessage {
public:
    static void showSuccess(QStatusBar* statusBar, const QString& message) {
        statusBar->setStyleSheet("QStatusBar { color: #4CAF50; }");
        statusBar->showMessage(message, 3000);
    }
    
    static void showError(QStatusBar* statusBar, const QString& message) {
        statusBar->setStyleSheet("QStatusBar { color: #F44336; }");
        statusBar->showMessage(message, 3000);
    }
};

} // namespace reqdb::gui
