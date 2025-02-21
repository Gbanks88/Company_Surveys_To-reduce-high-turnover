#include <gtest/gtest.h>
#include <QApplication>
#include "gui/ProjectView.hpp"

using namespace reqdb::gui;

TEST(ProjectViewTest, Creation) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    ProjectView view;
    EXPECT_TRUE(view.isEnabled());
}

TEST(ProjectViewTest, TreeView) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    ProjectView view;
    EXPECT_TRUE(view.treeView() != nullptr);
}
