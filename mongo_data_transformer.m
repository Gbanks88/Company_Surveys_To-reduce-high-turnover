% MongoDB Data Transformation and Processing Utilities
classdef MongoDataTransformer
    properties
        connection
    end
    
    methods
        function obj = MongoDataTransformer(mongoConn)
            obj.connection = mongoConn;
        end
        
        function normalized = normalizeSkillMetrics(obj, data)
            % Normalize skill metrics to standard scale
            try
                % Get skill fields
                skillFields = {'technicalSkills', 'softSkills', 'leadershipSkills'};
                
                % Initialize normalized structure
                normalized = data;
                
                % Normalize each skill field
                for i = 1:length(skillFields)
                    if isfield(data, skillFields{i})
                        values = [data.(skillFields{i})];
                        minVal = min(values);
                        maxVal = max(values);
                        
                        % Apply min-max normalization
                        normalized_values = (values - minVal) / (maxVal - minVal) * 100;
                        
                        % Update normalized structure
                        for j = 1:length(data)
                            normalized(j).(skillFields{i}) = normalized_values(j);
                        end
                    end
                end
            catch ME
                fprintf('Error normalizing skill metrics: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function enriched = enrichEmployeeData(obj, data)
            % Enrich employee data with additional metrics
            try
                enriched = data;
                
                for i = 1:length(data)
                    % Calculate skill growth rate
                    if isfield(data(i), 'skillHistory')
                        history = data(i).skillHistory;
                        enriched(i).skillGrowthRate = calculateGrowthRate(history);
                    end
                    
                    % Calculate certification completion rate
                    if isfield(data(i), 'certifications')
                        certs = data(i).certifications;
                        completed = sum([certs.completed]);
                        total = length(certs);
                        enriched(i).certCompletionRate = (completed / total) * 100;
                    end
                    
                    % Add performance percentile
                    if isfield(data(i), 'performanceScore')
                        allScores = [data.performanceScore];
                        enriched(i).performancePercentile = ...
                            percentilerank(allScores, data(i).performanceScore);
                    end
                    
                    % Calculate engagement score
                    if all(isfield(data(i), {'attendance', 'participation', 'initiative'}))
                        enriched(i).engagementScore = calculateEngagementScore(data(i));
                    end
                end
            catch ME
                fprintf('Error enriching employee data: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function transformed = transformSurveyResponses(obj, responses)
            % Transform survey responses into analyzable format
            try
                % Initialize transformed structure
                transformed = struct();
                
                % Group responses by category
                categories = unique({responses.category});
                for i = 1:length(categories)
                    cat = categories{i};
                    catResponses = responses([responses.category] == cat);
                    
                    % Calculate metrics for category
                    transformed.(cat) = struct(...
                        'meanScore', mean([catResponses.score]), ...
                        'stdDev', std([catResponses.score]), ...
                        'responses', length(catResponses), ...
                        'distribution', histcounts([catResponses.score], 5), ...
                        'trends', calculateTrends(catResponses) ...
                    );
                end
            catch ME
                fprintf('Error transforming survey responses: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function aggregated = aggregateTeamMetrics(obj, teamData)
            % Aggregate and analyze team-level metrics
            try
                % Group by team
                teams = unique([teamData.teamId]);
                
                % Initialize aggregated structure
                aggregated = struct('teams', cell(1, length(teams)));
                
                for i = 1:length(teams)
                    teamMembers = teamData([teamData.teamId] == teams(i));
                    
                    % Calculate team metrics
                    aggregated.teams(i) = struct(...
                        'teamId', teams(i), ...
                        'size', length(teamMembers), ...
                        'avgPerformance', mean([teamMembers.performanceScore]), ...
                        'skillDistribution', analyzeSkillDistribution(teamMembers), ...
                        'certificationStatus', analyzeCertifications(teamMembers), ...
                        'collaborationScore', calculateCollaborationScore(teamMembers) ...
                    );
                end
            catch ME
                fprintf('Error aggregating team metrics: %s\n', ME.message);
                rethrow(ME);
            end
        end
    end
    
    methods (Static)
        function rate = calculateGrowthRate(history)
            % Calculate growth rate from historical data
            scores = [history.score];
            times = [history.timestamp];
            
            % Fit linear regression
            p = polyfit(times, scores, 1);
            rate = p(1); % Slope represents growth rate
        end
        
        function score = calculateEngagementScore(employee)
            % Calculate employee engagement score
            weights = [0.4, 0.3, 0.3]; % Weights for different factors
            factors = [employee.attendance, ...
                      employee.participation, ...
                      employee.initiative];
            
            score = sum(weights .* factors);
        end
        
        function trends = calculateTrends(responses)
            % Calculate response trends over time
            dates = [responses.timestamp];
            scores = [responses.score];
            
            % Sort by date
            [dates, idx] = sort(dates);
            scores = scores(idx);
            
            % Calculate moving average
            windowSize = min(5, length(scores));
            trends = movmean(scores, windowSize);
        end
        
        function distribution = analyzeSkillDistribution(teamMembers)
            % Analyze skill distribution in team
            skills = {'technical', 'soft', 'leadership'};
            distribution = struct();
            
            for i = 1:length(skills)
                skillScores = [teamMembers.([skills{i} 'Skills'])];
                distribution.(skills{i}) = struct(...
                    'mean', mean(skillScores), ...
                    'std', std(skillScores), ...
                    'min', min(skillScores), ...
                    'max', max(skillScores), ...
                    'quartiles', prctile(skillScores, [25 50 75]) ...
                );
            end
        end
    end
end
