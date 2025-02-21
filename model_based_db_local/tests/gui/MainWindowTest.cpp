#include <gtest/gtest.h>
#include <QApplication>
#include "gui/MainWindow.hpp"
#include "db/DatabaseManager.hpp"

using namespace reqdb::gui;
using namespace reqdb::db;

TEST(MainWindowTest, Creation) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    DatabaseManager dbManager(":memory:");
    MainWindow window(&dbManager);
    EXPECT_TRUE(window.isEnabled());
}

TEST(MainWindowTest, MenuActions) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    DatabaseManager dbManager(":memory:");
    MainWindow window(&dbManager);
    EXPECT_TRUE(window.menuBar() != nullptr);
}
