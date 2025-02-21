% MongoDB Authentication and Security Manager
classdef MongoAuthManager
    properties (Access = private)
        configPath
        credentials
    end
    
    methods
        function obj = MongoAuthManager(configPath)
            if nargin < 1
                obj.configPath = 'mongo_config.json';
            else
                obj.configPath = configPath;
            end
            obj.credentials = struct();
        end
        
        function connectionString = getSecureConnectionString(obj)
            % Load and validate credentials
            obj.loadCredentials();
            
            % Build secure connection string
            connectionString = sprintf('mongodb://%s:%s@%s:%d/%s?authSource=%s&authMechanism=%s', ...
                obj.credentials.username, ...
                obj.credentials.password, ...
                obj.credentials.host, ...
                obj.credentials.port, ...
                obj.credentials.database, ...
                obj.credentials.authSource, ...
                obj.credentials.authMechanism);
            
            % Add SSL if enabled
            if obj.credentials.ssl
                connectionString = [connectionString '&ssl=true'];
                if ~isempty(obj.credentials.sslCAFile)
                    connectionString = [connectionString '&sslCAFile=' obj.credentials.sslCAFile];
                end
            end
        end
        
        function success = validateConnection(obj, mongo)
            % Validate MongoDB connection
            try
                % Try to execute simple command
                mongo.Database('admin').runCommand('ping');
                success = true;
                fprintf('Connection validated successfully\n');
            catch ME
                success = false;
                fprintf('Connection validation failed: %s\n', ME.message);
            end
        end
        
        function encryptCredentials(obj, credentials)
            % Encrypt credentials before saving
            try
                % Create encryption key
                key = generateEncryptionKey();
                
                % Encrypt sensitive fields
                credentials.password = encrypt(credentials.password, key);
                
                % Save encrypted credentials
                obj.saveEncryptedConfig(credentials, key);
                fprintf('Credentials encrypted and saved successfully\n');
            catch ME
                fprintf('Error encrypting credentials: %s\n', ME.message);
                rethrow(ME);
            end
        end
    end
    
    methods (Access = private)
        function loadCredentials(obj)
            % Load and decrypt credentials
            try
                if ~isfile(obj.configPath)
                    error('Configuration file not found');
                end
                
                % Read encrypted config
                fid = fopen(obj.configPath, 'r');
                raw = fread(fid, '*char')';
                fclose(fid);
                
                config = jsondecode(raw);
                
                % Decrypt sensitive fields
                key = obj.loadEncryptionKey();
                config.password = decrypt(config.password, key);
                
                % Validate configuration
                obj.validateConfig(config);
                
                obj.credentials = config;
            catch ME
                fprintf('Error loading credentials: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function validateConfig(~, config)
            % Validate configuration fields
            required = {'username', 'password', 'host', 'port', ...
                       'database', 'authSource', 'authMechanism', 'ssl'};
            
            for i = 1:length(required)
                if ~isfield(config, required{i})
                    error('Missing required field: %s', required{i});
                end
            end
            
            % Validate field types
            validateattributes(config.port, {'numeric'}, {'scalar', 'positive'});
            validateattributes(config.ssl, {'logical'}, {'scalar'});
        end
        
        function key = generateEncryptionKey()
            % Generate secure encryption key
            key = randbytes(32); % 256-bit key
        end
        
        function saveEncryptedConfig(obj, config, key)
            % Save encrypted configuration
            try
                % Save encryption key securely
                keyFile = [obj.configPath '.key'];
                fid = fopen(keyFile, 'w');
                fwrite(fid, key);
                fclose(fid);
                
                % Set secure file permissions
                if isunix
                    system(['chmod 600 ' keyFile]);
                end
                
                % Save encrypted config
                fid = fopen(obj.configPath, 'w');
                fprintf(fid, '%s', jsonencode(config));
                fclose(fid);
                
                if isunix
                    system(['chmod 600 ' obj.configPath]);
                end
            catch ME
                fprintf('Error saving encrypted configuration: %s\n', ME.message);
                rethrow(ME);
            end
        end
        
        function key = loadEncryptionKey(obj)
            % Load encryption key
            keyFile = [obj.configPath '.key'];
            if ~isfile(keyFile)
                error('Encryption key file not found');
            end
            
            fid = fopen(keyFile, 'r');
            key = fread(fid, '*uint8');
            fclose(fid);
        end
    end
end
