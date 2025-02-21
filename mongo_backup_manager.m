% MongoDB Backup and Recovery Manager
classdef MongoBackupManager
    properties
        connection
        backupDir
        encryptionKey
        retentionDays
    end
    
    methods
        function obj = MongoBackupManager(mongoConn, backupDir)
            obj.connection = mongoConn;
            obj.backupDir = backupDir;
            obj.retentionDays = 30; % Default retention period
            
            % Ensure backup directory exists
            if ~exist(backupDir, 'dir')
                mkdir(backupDir);
            end
            
            % Generate encryption key if not exists
            keyFile = fullfile(backupDir, 'backup.key');
            if ~exist(keyFile, 'file')
                obj.encryptionKey = obj.generateEncryptionKey();
                obj.saveEncryptionKey(keyFile);
            else
                obj.loadEncryptionKey(keyFile);
            end
        end
        
        function success = createBackup(obj, collections)
            % Create encrypted backup of specified collections
            try
                timestamp = datestr(now, 'yyyymmdd_HHMMSS');
                backupFile = fullfile(obj.backupDir, ['backup_' timestamp '.enc']);
                
                % Initialize backup structure
                backup = struct();
                
                % Export each collection
                for i = 1:length(collections)
                    collName = collections{i};
                    data = obj.connection.importSurveyData(struct()); % Get all documents
                    backup.(collName) = data;
                end
                
                % Add metadata
                backup.metadata = struct(...
                    'timestamp', timestamp, ...
                    'collections', {collections}, ...
                    'checksum', obj.calculateChecksum(backup) ...
                );
                
                % Encrypt and save backup
                obj.encryptAndSaveBackup(backup, backupFile);
                
                % Clean up old backups
                obj.cleanupOldBackups();
                
                success = true;
                fprintf('Backup created successfully: %s\n', backupFile);
            catch ME
                fprintf('Error creating backup: %s\n', ME.message);
                success = false;
            end
        end
        
        function success = restoreBackup(obj, backupFile, collections)
            % Restore data from backup file
            try
                % Load and decrypt backup
                backup = obj.loadAndDecryptBackup(backupFile);
                
                % Verify checksum
                if ~obj.verifyChecksum(backup)
                    error('Backup file integrity check failed');
                end
                
                % Restore each collection
                for i = 1:length(collections)
                    collName = collections{i};
                    if isfield(backup, collName)
                        % Create temporary collection name
                        tempColl = [collName '_restore_temp'];
                        
                        % Insert data into temporary collection
                        obj.connection.exportSurveyData(backup.(collName), ...
                            struct(), tempColl);
                        
                        % Verify restoration
                        if obj.verifyRestoration(collName, tempColl)
                            % Swap collections
                            obj.swapCollections(collName, tempColl);
                        else
                            error('Restoration verification failed for %s', collName);
                        end
                    end
                end
                
                success = true;
                fprintf('Backup restored successfully from: %s\n', backupFile);
            catch ME
                fprintf('Error restoring backup: %s\n', ME.message);
                success = false;
            end
        end
        
        function setRetentionPolicy(obj, days)
            % Set backup retention period
            obj.retentionDays = days;
            fprintf('Backup retention period set to %d days\n', days);
        end
        
        function verifyBackups(obj)
            % Verify integrity of all backup files
            try
                files = dir(fullfile(obj.backupDir, 'backup_*.enc'));
                
                fprintf('Verifying %d backup files...\n', length(files));
                for i = 1:length(files)
                    backupFile = fullfile(obj.backupDir, files(i).name);
                    backup = obj.loadAndDecryptBackup(backupFile);
                    
                    if obj.verifyChecksum(backup)
                        fprintf('✓ %s: Integrity verified\n', files(i).name);
                    else
                        fprintf('✗ %s: Integrity check failed\n', files(i).name);
                    end
                end
            catch ME
                fprintf('Error verifying backups: %s\n', ME.message);
            end
        end
    end
    
    methods (Access = private)
        function key = generateEncryptionKey(~)
            % Generate secure encryption key
            key = randbytes(32); % 256-bit key
        end
        
        function saveEncryptionKey(obj, keyFile)
            % Save encryption key securely
            fid = fopen(keyFile, 'w');
            fwrite(fid, obj.encryptionKey);
            fclose(fid);
            
            % Set secure permissions
            if isunix
                system(['chmod 600 ' keyFile]);
            end
        end
        
        function loadEncryptionKey(obj, keyFile)
            % Load encryption key
            fid = fopen(keyFile, 'r');
            obj.encryptionKey = fread(fid, '*uint8');
            fclose(fid);
        end
        
        function checksum = calculateChecksum(~, data)
            % Calculate SHA-256 checksum of data
            json = jsonencode(data);
            checksum = DataHash(json, 'SHA-256');
        end
        
        function encryptAndSaveBackup(obj, data, filename)
            % Encrypt and save backup data
            json = jsonencode(data);
            encrypted = encrypt(json, obj.encryptionKey);
            
            fid = fopen(filename, 'w');
            fwrite(fid, encrypted);
            fclose(fid);
        end
        
        function data = loadAndDecryptBackup(obj, filename)
            % Load and decrypt backup data
            fid = fopen(filename, 'r');
            encrypted = fread(fid, '*uint8');
            fclose(fid);
            
            json = decrypt(encrypted, obj.encryptionKey);
            data = jsondecode(json);
        end
        
        function success = verifyChecksum(obj, backup)
            % Verify backup data integrity
            storedChecksum = backup.metadata.checksum;
            backup.metadata = rmfield(backup.metadata, 'checksum');
            calculatedChecksum = obj.calculateChecksum(backup);
            
            success = isequal(storedChecksum, calculatedChecksum);
        end
        
        function cleanupOldBackups(obj)
            % Remove backups older than retention period
            files = dir(fullfile(obj.backupDir, 'backup_*.enc'));
            
            for i = 1:length(files)
                backupDate = datetime(files(i).date);
                if days(now - backupDate) > obj.retentionDays
                    delete(fullfile(obj.backupDir, files(i).name));
                    fprintf('Deleted old backup: %s\n', files(i).name);
                end
            end
        end
        
        function success = verifyRestoration(obj, origColl, tempColl)
            % Verify restored data matches original
            origData = obj.connection.importSurveyData(struct(), origColl);
            tempData = obj.connection.importSurveyData(struct(), tempColl);
            
            success = isequal(origData, tempData);
        end
        
        function swapCollections(obj, origColl, tempColl)
            % Atomically swap original and temporary collections
            obj.connection.database.renameCollection(origColl, [origColl '_old']);
            obj.connection.database.renameCollection(tempColl, origColl);
            obj.connection.database.dropCollection([origColl '_old']);
        end
    end
end
