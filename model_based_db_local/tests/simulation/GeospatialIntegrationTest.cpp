#include <gtest/gtest.h>
#include "simulation/GeospatialIntegration.hpp"

using namespace reqdb::simulation;

TEST(GeospatialIntegrationTest, Initialization) {
    GeospatialIntegration geo;
    EXPECT_TRUE(geo.initialize());
}

TEST(GeospatialIntegrationTest, CoordinateTransformation) {
    GeospatialIntegration geo;
    EXPECT_TRUE(geo.initialize());
    
    auto result = geo.transformCoordinates(45.0, -122.0, "EPSG:4326", "EPSG:3857");
    EXPECT_TRUE(result.has_value());
}
