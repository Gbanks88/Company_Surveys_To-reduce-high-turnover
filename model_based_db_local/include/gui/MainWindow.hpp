#pragma once

#include <QMainWindow>

namespace reqdb {
namespace gui {

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = nullptr);

private slots:
    void newProject();
    void openProject();

private:
    void setupUi();
    void createMenuBar();
    void setupStatusBar();
};

} // namespace gui
} // namespace reqdb
