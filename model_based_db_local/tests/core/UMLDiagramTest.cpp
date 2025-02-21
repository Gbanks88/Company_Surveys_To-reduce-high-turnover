#include <gtest/gtest.h>
#include "core/UMLDiagram.hpp"

using namespace reqdb::core;

TEST(UMLDiagramTest, BasicProperties) {
    UMLDiagram diagram;
    diagram.setTitle("Test Diagram");
    diagram.setDescription("Test Description");
    
    EXPECT_EQ(diagram.getTitle(), "Test Diagram");
    EXPECT_EQ(diagram.getDescription(), "Test Description");
}

TEST(UMLDiagramTest, Serialization) {
    UMLDiagram diagram;
    diagram.setTitle("Test Diagram");
    diagram.setDescription("Test Description");
    
    auto json = diagram.toJson();
    EXPECT_EQ(json["title"], "Test Diagram");
    EXPECT_EQ(json["description"], "Test Description");
    
    UMLDiagram diagram2;
    diagram2.fromJson(json);
    EXPECT_EQ(diagram2.getTitle(), diagram.getTitle());
    EXPECT_EQ(diagram2.getDescription(), diagram.getDescription());
}
