% IBM Credentials Validation Script
classdef IBMCredentialsValidator
    properties (Access = private)
        envFile
        credentials
    end
    
    methods
        function obj = IBMCredentialsValidator(envPath)
            obj.envFile = envPath;
            obj.credentials = obj.loadCredentials();
        end
        
        function status = validateAll(obj)
            % Validate all IBM credentials
            try
                status = struct();
                
                % Validate Cloud Object Storage
                status.cos = obj.validateCOS();
                
                % Log validation results
                obj.logValidationResults(status);
                
            catch ME
                fprintf('Error during validation: %s\n', ME.message);
                status.error = ME.message;
            end
        end
        
        function cosStatus = validateCOS(obj)
            % Validate IBM Cloud Object Storage credentials
            try
                cosStatus = struct('valid', false, 'message', '');
                
                % Check required COS credentials
                required = {'IBM_COS_ENDPOINT', 'IBM_COS_API_KEY', ...
                          'IBM_COS_INSTANCE_ID', 'IBM_COS_BUCKET_NAME'};
                
                % Verify all required fields exist
                for i = 1:length(required)
                    field = required{i};
                    if ~isfield(obj.credentials, field) || isempty(obj.credentials.(field))
                        cosStatus.message = sprintf('Missing required field: %s', field);
                        return;
                    end
                end
                
                % Test COS connection
                if obj.testCOSConnection()
                    cosStatus.valid = true;
                    cosStatus.message = 'COS credentials validated successfully';
                else
                    cosStatus.message = 'Failed to connect to COS';
                end
                
            catch ME
                cosStatus.message = sprintf('Error validating COS: %s', ME.message);
            end
        end
        
        function success = testCOSConnection(obj)
            % Test connection to IBM Cloud Object Storage
            try
                % Create COS client
                endpoint = obj.credentials.IBM_COS_ENDPOINT;
                apiKey = obj.credentials.IBM_COS_API_KEY;
                instanceId = obj.credentials.IBM_COS_INSTANCE_ID;
                bucketName = obj.credentials.IBM_COS_BUCKET_NAME;
                
                % Attempt to list bucket contents
                command = sprintf('curl -X GET "%s/%s" -H "Authorization: Bearer %s"', ...
                    endpoint, bucketName, apiKey);
                
                [status, ~] = system(command);
                success = (status == 0);
                
            catch ME
                fprintf('Error testing COS connection: %s\n', ME.message);
                success = false;
            end
        end
    end
    
    methods (Access = private)
        function credentials = loadCredentials(obj)
            % Load credentials from .env file
            try
                credentials = struct();
                
                % Read .env file
                fid = fopen(obj.envFile, 'r');
                if fid == -1
                    error('Could not open .env file');
                end
                
                % Parse each line
                while ~feof(fid)
                    line = fgetl(fid);
                    if ischar(line) && ~isempty(line) && line(1) ~= '#'
                        parts = strsplit(line, '=');
                        if length(parts) == 2
                            key = strtrim(parts{1});
                            value = strtrim(parts{2});
                            credentials.(key) = value;
                        end
                    end
                end
                
                fclose(fid);
                
            catch ME
                fprintf('Error loading credentials: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function logValidationResults(obj, status)
            % Log validation results
            try
                logFile = 'ibm_validation.log';
                fid = fopen(logFile, 'a');
                
                fprintf(fid, '\n=== Validation Results (%s) ===\n', ...
                    datestr(now, 'yyyy-mm-dd HH:MM:SS'));
                
                % Log COS status
                fprintf(fid, 'Cloud Object Storage:\n');
                fprintf(fid, '  Valid: %d\n', status.cos.valid);
                fprintf(fid, '  Message: %s\n', status.cos.message);
                
                fclose(fid);
                
            catch ME
                fprintf('Error logging validation results: %s\n', ME.message);
            end
        end
    end
end
