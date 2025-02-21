#include <gtest/gtest.h>
#include <QApplication>
#include "gui/DiagramEditor.hpp"

using namespace reqdb::gui;

TEST(DiagramEditorTest, Creation) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    DiagramEditor editor;
    EXPECT_TRUE(editor.isEnabled());
}

TEST(DiagramEditorTest, ToolbarActions) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    DiagramEditor editor;
    EXPECT_TRUE(editor.toolBar() != nullptr);
}
