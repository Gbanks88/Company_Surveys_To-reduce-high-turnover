% MongoDB Connection and Data Management via Studio 3T
classdef MongoConnection
    properties
        mongo
        database
        collection
        connectionString
    end
    
    methods
        function obj = MongoConnection()
            % Initialize MongoDB connection parameters
            obj.connectionString = 'mongodb://localhost:27017';
        end
        
        function obj = connect(obj, dbName, collectionName)
            try
                % Create MongoDB connection
                obj.mongo = mongodb(obj.connectionString);
                
                % Select database and collection
                obj.database = obj.mongo.Database(dbName);
                obj.collection = obj.database.Collection(collectionName);
                
                fprintf('Successfully connected to MongoDB database: %s\n', dbName);
            catch ME
                fprintf('Error connecting to MongoDB: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function data = importSurveyData(obj, query)
            % Import survey data from MongoDB
            try
                % Execute query
                cursor = obj.collection.find(query);
                
                % Convert to MATLAB table
                data = table();
                while cursor.hasNext()
                    document = cursor.next();
                    
                    % Convert document to struct
                    docStruct = document.toStruct();
                    
                    % Append to table
                    if isempty(data)
                        data = struct2table(docStruct);
                    else
                        data = [data; struct2table(docStruct)];
                    end
                end
                
                fprintf('Successfully imported %d records\n', height(data));
            catch ME
                fprintf('Error importing data: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function exportSurveyData(obj, data, queryFilter)
            % Export survey data to MongoDB
            try
                % Convert MATLAB table to documents
                if istable(data)
                    documents = table2struct(data, 'ToScalar', true);
                else
                    documents = data;
                end
                
                % If filter provided, update existing documents
                if nargin > 2 && ~isempty(queryFilter)
                    for i = 1:length(documents)
                        obj.collection.update_one(queryFilter, ...
                            {'$set', documents(i)}, ...
                            'Upsert', true);
                    end
                else
                    % Insert new documents
                    obj.collection.insert_many(documents);
                end
                
                fprintf('Successfully exported data to MongoDB\n');
            catch ME
                fprintf('Error exporting data: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function aggregateData(obj, pipeline)
            % Perform MongoDB aggregation
            try
                cursor = obj.collection.aggregate(pipeline);
                
                % Process results
                results = table();
                while cursor.hasNext()
                    document = cursor.next();
                    if isempty(results)
                        results = struct2table(document.toStruct());
                    else
                        results = [results; struct2table(document.toStruct())];
                    end
                end
                
                % Display results
                disp(results);
            catch ME
                fprintf('Error performing aggregation: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function close(obj)
            % Close MongoDB connection
            try
                obj.mongo.close();
                fprintf('MongoDB connection closed\n');
            catch ME
                fprintf('Error closing connection: %s\n', ME.message);
            end
        end
    end
end
