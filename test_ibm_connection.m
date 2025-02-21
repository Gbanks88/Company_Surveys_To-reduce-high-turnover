% Test IBM Cloud Object Storage Connection
function test_ibm_connection()
    try
        % Initialize validator
        validator = IBMCredentialsValidator(fullfile(pwd, '.env'));
        
        % Validate credentials
        status = validator.validateAll();
        
        % Display results
        disp('=== IBM Credentials Validation Results ===');
        
        % Display COS results
        disp('Cloud Object Storage:');
        disp(['  Valid: ' num2str(status.cos.valid)]);
        disp(['  Message: ' status.cos.message]);
        
    catch ME
        fprintf('Error testing IBM connection: %s\n', ME.message);
    end
end
