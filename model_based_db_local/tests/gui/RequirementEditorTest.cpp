#include <gtest/gtest.h>
#include <QApplication>
#include "gui/RequirementEditor.hpp"

using namespace reqdb::gui;

TEST(RequirementEditorTest, Creation) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    RequirementEditor editor;
    EXPECT_TRUE(editor.isEnabled());
}

TEST(RequirementEditorTest, FormElements) {
    int argc = 1;
    char* argv[] = {(char*)"test"};
    QApplication app(argc, argv);
    
    RequirementEditor editor;
    EXPECT_TRUE(editor.layout() != nullptr);
}
