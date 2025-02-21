% Survey Data Import and Preprocessing
classdef SurveyDataImport
    properties
        weeklyData
        quarterlyData
        yearlyData
        employeeInfo
    end
    
    methods
        function obj = SurveyDataImport()
            % Initialize data structures
            obj.weeklyData = struct();
            obj.quarterlyData = struct();
            obj.yearlyData = struct();
            obj.employeeInfo = struct();
        end
        
        function obj = importCSVData(obj, filename, dataType)
            % Import CSV data based on survey type
            try
                data = readtable(filename);
                switch dataType
                    case 'weekly'
                        obj.weeklyData = data;
                    case 'quarterly'
                        obj.quarterlyData = data;
                    case 'yearly'
                        obj.yearlyData = data;
                    case 'employee'
                        obj.employeeInfo = data;
                end
            catch ME
                fprintf('Error importing %s data: %s\n', dataType, ME.message);
            end
        end
        
        function cleanedData = preprocessData(obj, data)
            % Clean and preprocess survey data
            cleanedData = data;
            
            % Remove missing values
            cleanedData = rmmissing(cleanedData);
            
            % Remove outliers using IQR method
            numericCols = varfun(@isnumeric, cleanedData, 'OutputFormat', 'cell');
            for i = 1:width(cleanedData)
                if numericCols{i}
                    col = cleanedData{:,i};
                    Q1 = prctile(col, 25);
                    Q3 = prctile(col, 75);
                    IQR = Q3 - Q1;
                    outliers = col < (Q1 - 1.5*IQR) | col > (Q3 + 1.5*IQR);
                    cleanedData{outliers,i} = NaN;
                end
            end
            
            % Normalize numeric columns to 0-100 scale
            for i = 1:width(cleanedData)
                if numericCols{i}
                    col = cleanedData{:,i};
                    cleanedData{:,i} = (col - min(col)) / (max(col) - min(col)) * 100;
                end
            end
        end
    end
end
