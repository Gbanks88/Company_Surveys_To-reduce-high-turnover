% Automated Backup Scheduler for MongoDB
classdef BackupScheduler
    properties
        backupManager
        schedules
        logFile
        isRunning
        taskQueue
    end
    
    methods
        function obj = BackupScheduler(backupManager)
            obj.backupManager = backupManager;
            obj.schedules = containers.Map();
            obj.logFile = fullfile(backupManager.backupDir, 'backup_scheduler.log');
            obj.isRunning = false;
            obj.taskQueue = parallel.pool.DataQueue;
            
            % Initialize logging
            obj.initializeLogger();
        end
        
        function schedule(obj, jobName, collections, interval, startTime)
            % Schedule a new backup job
            try
                if ~obj.isValidInterval(interval)
                    error('Invalid interval format. Use format: daily|weekly|monthly HH:MM');
                end
                
                job = struct(...
                    'name', jobName, ...
                    'collections', {collections}, ...
                    'interval', interval, ...
                    'startTime', startTime, ...
                    'lastRun', [], ...
                    'nextRun', obj.calculateNextRun(interval, startTime) ...
                );
                
                obj.schedules(jobName) = job;
                obj.log(sprintf('Scheduled new backup job: %s', jobName));
                
                % Start scheduler if not running
                if ~obj.isRunning
                    obj.start();
                end
            catch ME
                obj.log(sprintf('Error scheduling backup job: %s', ME.message));
                rethrow(ME);
            end
        end
        
        function start(obj)
            % Start the backup scheduler
            try
                if ~obj.isRunning
                    obj.isRunning = true;
                    obj.log('Backup scheduler started');
                    
                    % Start background worker
                    afterEach(obj.taskQueue, @(data) obj.processTask(data));
                    obj.scheduleNextTask();
                end
            catch ME
                obj.log(sprintf('Error starting scheduler: %s', ME.message));
                obj.isRunning = false;
                rethrow(ME);
            end
        end
        
        function stop(obj)
            % Stop the backup scheduler
            try
                if obj.isRunning
                    obj.isRunning = false;
                    obj.log('Backup scheduler stopped');
                    delete(obj.taskQueue);
                end
            catch ME
                obj.log(sprintf('Error stopping scheduler: %s', ME.message));
                rethrow(ME);
            end
        end
        
        function status = getStatus(obj)
            % Get current scheduler status
            status = struct(...
                'isRunning', obj.isRunning, ...
                'jobCount', obj.schedules.Count, ...
                'nextBackup', obj.getNextBackupTime(), ...
                'jobs', obj.getJobStatus() ...
            );
        end
        
        function modifySchedule(obj, jobName, newInterval, newStartTime)
            % Modify an existing backup schedule
            try
                if obj.schedules.isKey(jobName)
                    job = obj.schedules(jobName);
                    job.interval = newInterval;
                    job.startTime = newStartTime;
                    job.nextRun = obj.calculateNextRun(newInterval, newStartTime);
                    
                    obj.schedules(jobName) = job;
                    obj.log(sprintf('Modified schedule for job: %s', jobName));
                    
                    % Reschedule next task
                    obj.scheduleNextTask();
                else
                    error('Job not found: %s', jobName);
                end
            catch ME
                obj.log(sprintf('Error modifying schedule: %s', ME.message));
                rethrow(ME);
            end
        end
        
        function removeSchedule(obj, jobName)
            % Remove a backup schedule
            try
                if obj.schedules.isKey(jobName)
                    obj.schedules.remove(jobName);
                    obj.log(sprintf('Removed backup schedule: %s', jobName));
                    
                    % Reschedule next task if needed
                    if obj.schedules.Count > 0
                        obj.scheduleNextTask();
                    else
                        obj.stop();
                    end
                end
            catch ME
                obj.log(sprintf('Error removing schedule: %s', ME.message));
                rethrow(ME);
            end
        end
    end
    
    methods (Access = private)
        function initializeLogger(obj)
            % Initialize logging system
            try
                if ~exist(obj.logFile, 'file')
                    fid = fopen(obj.logFile, 'w');
                    fprintf(fid, 'Backup Scheduler Log\n');
                    fprintf(fid, '===================\n\n');
                    fclose(fid);
                end
            catch ME
                warning('Failed to initialize logger: %s', ME.message);
            end
        end
        
        function log(obj, message)
            % Log a message with timestamp
            try
                timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
                logMessage = sprintf('[%s] %s\n', timestamp, message);
                
                fid = fopen(obj.logFile, 'a');
                fprintf(fid, '%s', logMessage);
                fclose(fid);
            catch ME
                warning('Failed to log message: %s', ME.message);
            end
        end
        
        function valid = isValidInterval(~, interval)
            % Validate backup interval format
            parts = strsplit(interval, ' ');
            if length(parts) ~= 2
                valid = false;
                return;
            end
            
            period = parts{1};
            time = parts{2};
            
            valid = any(strcmp(period, {'daily', 'weekly', 'monthly'})) && ...
                   ~isempty(regexp(time, '^\d{2}:\d{2}$', 'once'));
        end
        
        function nextRun = calculateNextRun(~, interval, startTime)
            % Calculate next run time based on interval
            parts = strsplit(interval, ' ');
            period = parts{1};
            timeStr = parts{2};
            
            now = datetime('now');
            [hour, minute] = deal(str2double(timeStr(1:2)), str2double(timeStr(4:5)));
            
            switch period
                case 'daily'
                    nextRun = datetime(now.Year, now.Month, now.Day, hour, minute, 0);
                case 'weekly'
                    nextRun = datetime(now.Year, now.Month, now.Day, hour, minute, 0);
                    nextRun = nextRun + days(7 - weekday(nextRun) + 1);
                case 'monthly'
                    nextRun = datetime(now.Year, now.Month, 1, hour, minute, 0);
                    if nextRun < now
                        nextRun = nextRun + calmonths(1);
                    end
            end
            
            if nextRun <= now
                switch period
                    case 'daily'
                        nextRun = nextRun + days(1);
                    case 'weekly'
                        nextRun = nextRun + days(7);
                    case 'monthly'
                        nextRun = nextRun + calmonths(1);
                end
            end
        end
        
        function scheduleNextTask(obj)
            % Schedule the next backup task
            if obj.isRunning && obj.schedules.Count > 0
                nextJob = obj.findNextJob();
                if ~isempty(nextJob)
                    send(obj.taskQueue, nextJob);
                end
            end
        end
        
        function processTask(obj, job)
            % Process a backup task
            try
                obj.log(sprintf('Starting backup for job: %s', job.name));
                
                % Perform backup
                success = obj.backupManager.createBackup(job.collections);
                
                % Update job status
                job.lastRun = datetime('now');
                job.nextRun = obj.calculateNextRun(job.interval, job.startTime);
                obj.schedules(job.name) = job;
                
                % Log result
                if success
                    obj.log(sprintf('Backup completed successfully for job: %s', job.name));
                else
                    obj.log(sprintf('Backup failed for job: %s', job.name));
                end
                
                % Schedule next task
                obj.scheduleNextTask();
            catch ME
                obj.log(sprintf('Error processing backup task: %s', ME.message));
            end
        end
        
        function nextJob = findNextJob(obj)
            % Find the next job to execute
            nextJob = [];
            nextTime = datetime('infinity');
            
            keys = obj.schedules.keys;
            for i = 1:length(keys)
                job = obj.schedules(keys{i});
                if job.nextRun < nextTime
                    nextTime = job.nextRun;
                    nextJob = job;
                end
            end
        end
        
        function nextTime = getNextBackupTime(obj)
            % Get the next scheduled backup time
            nextJob = obj.findNextJob();
            if ~isempty(nextJob)
                nextTime = nextJob.nextRun;
            else
                nextTime = [];
            end
        end
        
        function status = getJobStatus(obj)
            % Get status of all scheduled jobs
            keys = obj.schedules.keys;
            status = struct('jobs', cell(1, length(keys)));
            
            for i = 1:length(keys)
                job = obj.schedules(keys{i});
                status.jobs(i) = struct(...
                    'name', job.name, ...
                    'collections', {job.collections}, ...
                    'interval', job.interval, ...
                    'lastRun', job.lastRun, ...
                    'nextRun', job.nextRun ...
                );
            end
        end
    end
end
