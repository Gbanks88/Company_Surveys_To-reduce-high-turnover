// Studio 3T Example Queries for Survey Analytics
// Copy and paste these queries into Studio 3T's IntelliShell

// 1. Find Recent Survey Responses with Sentiment Analysis
db.processed_data.find({
    'model_info.type': 'sentiment_analysis',
    'timestamp': {
        $gte: new Date(new Date().setDate(new Date().getDate() - 30))
    }
}).sort({ timestamp: -1 })

// 2. Aggregate Sentiment by Department
db.processed_data.aggregate([
    {
        $match: {
            'model_info.type': 'sentiment_analysis'
        }
    },
    {
        $group: {
            _id: '$data.department',
            avgSentiment: { $avg: '$data.sentiment.score' },
            totalResponses: { $sum: 1 }
        }
    },
    {
        $sort: { avgSentiment: -1 }
    }
])

// 3. Find Top Employee Concerns (Keywords)
db.processed_data.aggregate([
    {
        $match: {
            'model_info.type': 'keyword_extraction'
        }
    },
    {
        $unwind: '$data.keywords'
    },
    {
        $group: {
            _id: '$data.keywords.text',
            frequency: { $sum: 1 },
            relevance: { $avg: '$data.keywords.relevance' }
        }
    },
    {
        $sort: { frequency: -1 }
    },
    {
        $limit: 10
    }
])

// 4. Track Model Performance Over Time
db.model_artifacts.aggregate([
    {
        $match: {
            'metadata.metrics': { $exists: true }
        }
    },
    {
        $group: {
            _id: {
                model: '$model_name',
                version: '$metadata.version'
            },
            avgAccuracy: { $avg: '$metadata.metrics.accuracy' },
            samples: { $sum: 1 }
        }
    },
    {
        $sort: { '_id.model': 1, '_id.version': -1 }
    }
])

// 5. Find Surveys Needing Attention (Low Sentiment)
db.processed_data.find({
    'model_info.type': 'sentiment_analysis',
    'data.sentiment.score': { $lt: -0.5 }
}, {
    'data.text': 1,
    'data.sentiment': 1,
    'data.department': 1,
    'timestamp': 1
}).sort({ 'data.sentiment.score': 1 })

// 6. Cross-Collection Analysis (Raw to Processed)
db.raw_survey_data.aggregate([
    {
        $lookup: {
            from: 'processed_data',
            localField: '_id',
            foreignField: 'source_id',
            as: 'analysis'
        }
    },
    {
        $match: {
            'analysis': { $ne: [] }
        }
    },
    {
        $project: {
            original_text: '$data.text',
            sentiment: { $arrayElemAt: ['$analysis.data.sentiment', 0] },
            keywords: { $arrayElemAt: ['$analysis.data.keywords', 0] }
        }
    }
])

// 7. Data Quality Check
db.raw_survey_data.aggregate([
    {
        $lookup: {
            from: 'processed_data',
            localField: '_id',
            foreignField: 'source_id',
            as: 'processed'
        }
    },
    {
        $group: {
            _id: null,
            total_raw: { $sum: 1 },
            processed_count: {
                $sum: { $cond: [{ $gt: [{ $size: '$processed' }, 0] }, 1, 0] }
            },
            unprocessed_count: {
                $sum: { $cond: [{ $eq: [{ $size: '$processed' }, 0] }, 1, 0] }
            }
        }
    },
    {
        $project: {
            _id: 0,
            total_raw: 1,
            processed_count: 1,
            unprocessed_count: 1,
            processing_rate: {
                $multiply: [
                    { $divide: ['$processed_count', '$total_raw'] },
                    100
                ]
            }
        }
    }
])

// 8. Time-based Analysis
db.processed_data.aggregate([
    {
        $match: {
            'model_info.type': 'sentiment_analysis'
        }
    },
    {
        $group: {
            _id: {
                year: { $year: '$timestamp' },
                month: { $month: '$timestamp' },
                week: { $week: '$timestamp' }
            },
            avgSentiment: { $avg: '$data.sentiment.score' },
            responses: { $sum: 1 }
        }
    },
    {
        $sort: { '_id.year': -1, '_id.month': -1, '_id.week': -1 }
    }
])
