% Example usage of MongoDB connection with survey system

% Initialize connection
mongo = MongoConnection();

try
    % Connect to database
    mongo.connect('employee_surveys', 'survey_responses');
    
    % Import weekly survey data
    weeklyQuery = struct('surveyType', 'weekly', ...
                        'date', struct('$gte', datestr(now-7, 'yyyy-mm-dd')));
    weeklyData = mongo.importSurveyData(weeklyQuery);
    
    % Import quarterly survey data
    quarterlyQuery = struct('surveyType', 'quarterly', ...
                          'quarter', getCurrentQuarter());
    quarterlyData = mongo.importSurveyData(quarterlyQuery);
    
    % Perform analysis
    analyzer = SurveyMetricsAnalysis(struct('weeklyData', weeklyData, ...
                                          'quarterlyData', quarterlyData));
    
    % Calculate metrics
    skillGrowth = analyzer.calculateSkillGrowth('weekly');
    promotionReadiness = analyzer.assessPromotionReadiness();
    
    % Create visualizations
    visualizer = SurveyVisualization(analyzer);
    visualizer.createDashboard(1001); % Example employee ID
    
    % Export results back to MongoDB
    results = struct('employeeId', 1001, ...
                    'skillGrowth', skillGrowth, ...
                    'promotionReadiness', promotionReadiness, ...
                    'analysisDate', datestr(now, 'yyyy-mm-dd'));
    
    mongo.exportSurveyData(results, struct('employeeId', 1001));
    
    % Perform aggregation for department-wide analysis
    pipeline = { ...
        struct('$match', struct('surveyType', 'quarterly')), ...
        struct('$group', struct('_id', '$department', ...
                              'avgPerformance', struct('$avg', '$performanceScore'), ...
                              'certifications', struct('$sum', '$certificationComplete'))) ...
    };
    
    mongo.aggregateData(pipeline);
    
catch ME
    fprintf('Error in survey analysis: %s\n', ME.message);
end

% Close connection
mongo.close();

function quarter = getCurrentQuarter()
    % Helper function to get current quarter
    currentMonth = month(now);
    quarter = ceil(currentMonth/3);
end
