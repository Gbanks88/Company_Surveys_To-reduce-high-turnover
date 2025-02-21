// Studio 3T Queries for Requirements Management

// 1. Find High Priority Requirements
db.requirements.find({
    priority: { $lte: 2 },
    status: { $in: ["draft", "review"] }
}).sort({ created_at: -1 })

// 2. Requirements by Type and Status
db.requirements.aggregate([
    {
        $group: {
            _id: {
                type: "$type",
                status: "$status"
            },
            count: { $sum: 1 },
            requirements: { $push: "$$ROOT" }
        }
    },
    {
        $sort: { "_id.type": 1, "_id.status": 1 }
    }
])

// 3. Use Cases Without Requirements
db.use_cases.find({
    $or: [
        { requirements: { $size: 0 } },
        { requirements: { $exists: false } }
    ]
})

// 4. Requirements Coverage Analysis
db.requirements.aggregate([
    {
        $lookup: {
            from: "use_cases",
            localField: "_id",
            foreignField: "requirements",
            as: "implementing_use_cases"
        }
    },
    {
        $project: {
            req_id: 1,
            title: 1,
            status: 1,
            coverage: { $size: "$implementing_use_cases" }
        }
    },
    {
        $match: {
            coverage: 0
        }
    }
])

// 5. Requirement Dependencies Graph
db.requirement_relationships.aggregate([
    {
        $graphLookup: {
            from: "requirement_relationships",
            startWith: "$source_id",
            connectFromField: "target_id",
            connectToField: "source_id",
            as: "dependency_chain",
            maxDepth: 5
        }
    },
    {
        $match: {
            dependency_chain: { $ne: [] }
        }
    }
])

// 6. Requirements Change History
db.requirement_history.aggregate([
    {
        $sort: { timestamp: -1 }
    },
    {
        $group: {
            _id: "$item_id",
            changes: { $push: "$$ROOT" },
            total_changes: { $sum: 1 },
            last_change: { $first: "$timestamp" }
        }
    },
    {
        $lookup: {
            from: "requirements",
            localField: "_id",
            foreignField: "_id",
            as: "requirement"
        }
    }
])

// 7. Stakeholder Impact Analysis
db.requirements.aggregate([
    {
        $unwind: "$stakeholders"
    },
    {
        $group: {
            _id: "$stakeholders",
            requirements: { $push: "$$ROOT" },
            total_requirements: { $sum: 1 },
            high_priority: {
                $sum: { $cond: [{ $lte: ["$priority", 2] }, 1, 0] }
            }
        }
    },
    {
        $sort: { high_priority: -1 }
    }
])

// 8. Use Case Complexity Analysis
db.use_cases.aggregate([
    {
        $project: {
            uc_id: 1,
            title: 1,
            complexity_score: {
                $add: [
                    { $size: "$main_flow" },
                    { $size: "$alternative_flows" },
                    { $size: "$preconditions" },
                    { $size: "$postconditions" },
                    { $size: "$requirements" }
                ]
            }
        }
    },
    {
        $sort: { complexity_score: -1 }
    }
])

// 9. Requirements Validation Status
db.requirements.aggregate([
    {
        $lookup: {
            from: "use_cases",
            localField: "_id",
            foreignField: "requirements",
            as: "use_cases"
        }
    },
    {
        $project: {
            req_id: 1,
            title: 1,
            status: 1,
            implementation_status: {
                $cond: {
                    if: { $eq: [{ $size: "$use_cases" }, 0] },
                    then: "not_implemented",
                    else: {
                        $cond: {
                            if: {
                                $allElementMatch: {
                                    $use_cases: { status: "tested" }
                                }
                            },
                            then: "fully_tested",
                            else: "partially_implemented"
                        }
                    }
                }
            }
        }
    }
])

// 10. Requirements Timeline Analysis
db.requirement_history.aggregate([
    {
        $match: {
            action: { $in: ["created", "status_updated"] }
        }
    },
    {
        $group: {
            _id: {
                year: { $year: { $toDate: "$timestamp" } },
                month: { $month: { $toDate: "$timestamp" } },
                week: { $week: { $toDate: "$timestamp" } }
            },
            new_requirements: {
                $sum: { $cond: [{ $eq: ["$action", "created"] }, 1, 0] }
            },
            status_changes: {
                $sum: { $cond: [{ $eq: ["$action", "status_updated"] }, 1, 0] }
            }
        }
    },
    {
        $sort: {
            "_id.year": -1,
            "_id.month": -1,
            "_id.week": -1
        }
    }
])
