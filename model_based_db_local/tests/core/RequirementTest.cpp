#include <gtest/gtest.h>
#include "core/Requirement.hpp"

using namespace reqdb::core;

TEST(RequirementTest, BasicProperties) {
    Requirement req;
    req.setTitle("Test Requirement");
    req.setDescription("Test Description");
    
    EXPECT_EQ(req.getTitle(), "Test Requirement");
    EXPECT_EQ(req.getDescription(), "Test Description");
}

TEST(RequirementTest, Serialization) {
    Requirement req;
    req.setTitle("Test Requirement");
    req.setDescription("Test Description");
    
    auto json = req.toJson();
    EXPECT_EQ(json["title"], "Test Requirement");
    EXPECT_EQ(json["description"], "Test Description");
    
    Requirement req2;
    req2.fromJson(json);
    EXPECT_EQ(req2.getTitle(), req.getTitle());
    EXPECT_EQ(req2.getDescription(), req.getDescription());
}
