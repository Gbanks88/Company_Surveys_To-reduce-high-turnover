// Studio 3T Queries for Model-Based Software Engineering

// 1. Find Latest UML Diagrams
db.uml_diagrams.find({})
    .sort({ timestamp: -1 })
    .limit(10)

// 2. Get Model Statistics
db.software_models.aggregate([
    {
        $group: {
            _id: '$type',
            count: { $sum: 1 },
            avgEntities: { $avg: '$metadata.entities_count' },
            avgRelationships: { $avg: '$metadata.relationships_count' }
        }
    }
])

// 3. Track Model Evolution
db.model_relationships.aggregate([
    {
        $group: {
            _id: {
                source: '$source',
                target: '$target'
            },
            relationTypes: { $addToSet: '$type' },
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
])

// 4. Find Complex Models
db.uml_diagrams.find({
    'metadata.entities_count': { $gt: 10 },
    'metadata.relationships_count': { $gt: 15 }
})

// 5. Analyze Model Changes Over Time
db.software_models.aggregate([
    {
        $group: {
            _id: {
                year: { $year: { $toDate: '$timestamp' } },
                month: { $month: { $toDate: '$timestamp' } }
            },
            modelCount: { $sum: 1 },
            avgComplexity: {
                $avg: {
                    $add: [
                        '$metadata.entities_count',
                        '$metadata.relationships_count'
                    ]
                }
            }
        }
    },
    {
        $sort: { '_id.year': -1, '_id.month': -1 }
    }
])

// 6. Find Related Models
db.model_relationships.aggregate([
    {
        $graphLookup: {
            from: 'model_relationships',
            startWith: '$source',
            connectFromField: 'target',
            connectToField: 'source',
            as: 'related_models',
            maxDepth: 3
        }
    },
    {
        $match: {
            'related_models': { $ne: [] }
        }
    }
])

// 7. Identify Isolated Components
db.software_models.aggregate([
    {
        $lookup: {
            from: 'model_relationships',
            localField: '_id',
            foreignField: 'source',
            as: 'outgoing'
        }
    },
    {
        $lookup: {
            from: 'model_relationships',
            localField: '_id',
            foreignField: 'target',
            as: 'incoming'
        }
    },
    {
        $match: {
            $and: [
                { outgoing: { $size: 0 } },
                { incoming: { $size: 0 } }
            ]
        }
    }
])

// 8. Export Diagram to DrawIO Format
db.uml_diagrams.findOne(
    { _id: ObjectId('your_diagram_id') },
    { content: 1 }
)
