#include <gtest/gtest.h>
#include "core/Traceability.hpp"

using namespace reqdb::core;

TEST(TraceabilityTest, BasicProperties) {
    Traceability trace;
    trace.setSourceId("REQ-001");
    trace.setTargetId("REQ-002");
    trace.setType("DEPENDS_ON");
    
    EXPECT_EQ(trace.getSourceId(), "REQ-001");
    EXPECT_EQ(trace.getTargetId(), "REQ-002");
    EXPECT_EQ(trace.getType(), "DEPENDS_ON");
}

TEST(TraceabilityTest, Serialization) {
    Traceability trace;
    trace.setSourceId("REQ-001");
    trace.setTargetId("REQ-002");
    trace.setType("DEPENDS_ON");
    
    auto json = trace.toJson();
    EXPECT_EQ(json["source_id"], "REQ-001");
    EXPECT_EQ(json["target_id"], "REQ-002");
    EXPECT_EQ(json["type"], "DEPENDS_ON");
    
    Traceability trace2;
    trace2.fromJson(json);
    EXPECT_EQ(trace2.getSourceId(), trace.getSourceId());
    EXPECT_EQ(trace2.getTargetId(), trace.getTargetId());
    EXPECT_EQ(trace2.getType(), trace.getType());
}
