import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

class IBMCredentialsValidator:
    def __init__(self, env_path='.env'):
        """Initialize IBM credentials validator."""
        self.env_path = env_path
        self.credentials = self._load_credentials()
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            filename='ibm_validation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _load_credentials(self):
        """Load credentials from .env file."""
        try:
            load_dotenv(self.env_path)
            return {
                'cos_endpoint': os.getenv('IBM_COS_ENDPOINT'),
                'cos_api_key': os.getenv('IBM_COS_API_KEY'),
                'cos_instance_id': os.getenv('IBM_COS_INSTANCE_ID'),
                'cos_bucket_name': os.getenv('IBM_COS_BUCKET_NAME')
            }
        except Exception as e:
            raise Exception(f"Error loading credentials: {str(e)}")

    def validate_all(self):
        """Validate all IBM credentials."""
        try:
            status = {
                'timestamp': datetime.now().isoformat(),
                'cos': self.validate_cos()
            }
            
            self._log_validation_results(status)
            return status
            
        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            return {'error': str(e)}

    def validate_cos(self):
        """Validate IBM Cloud Object Storage credentials."""
        try:
            status = {'valid': False, 'message': ''}

            # Check required fields
            required_fields = ['cos_endpoint', 'cos_api_key', 
                             'cos_instance_id', 'cos_bucket_name']
            
            for field in required_fields:
                if not self.credentials.get(field):
                    status['message'] = f'Missing required field: {field}'
                    self.logger.warning(status['message'])
                    return status

            # Test COS connection
            if self._test_cos_connection():
                status['valid'] = True
                status['message'] = 'COS credentials validated successfully'
            else:
                status['message'] = 'Failed to connect to COS'

            return status

        except Exception as e:
            return {'valid': False, 'message': f'Error validating COS: {str(e)}'}

    def _test_cos_connection(self):
        """Test connection to IBM Cloud Object Storage."""
        try:
            endpoint = self.credentials['cos_endpoint']
            bucket = self.credentials['cos_bucket_name']
            api_key = self.credentials['cos_api_key']

            # Get IAM token
            token_url = "https://iam.cloud.ibm.com/identity/token"
            token_response = requests.post(
                token_url,
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                    "apikey": api_key
                },
                headers={
                    "Accept": "application/json"
                }
            )
            
            if token_response.status_code != 200:
                self.logger.error(f"Failed to get IAM token. Status: {token_response.status_code}, Response: {token_response.text}")
                return False

            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                self.logger.error("No access token in response")
                return False

            # Test bucket access
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            # Remove quotes from endpoint if present
            endpoint = endpoint.strip("'").strip('"')
            bucket = bucket.strip("'").strip('"')
            
            bucket_url = f"{endpoint}/{bucket}"
            response = requests.head(bucket_url, headers=headers)
            
            if response.status_code not in [200, 403, 404]:  # 403/404 means bucket exists but we might not have access
                self.logger.error(f"Failed to access bucket. Status: {response.status_code}, Response: {response.text if hasattr(response, 'text') else 'No response text'}")
                return False
                
            return True

        except Exception as e:
            self.logger.error(f"Error testing COS connection: {str(e)}")
            return False

    def _log_validation_results(self, status):
        """Log validation results."""
        try:
            self.logger.info("=== Validation Results ===")
            self.logger.info(f"Timestamp: {status['timestamp']}")
            
            if 'cos' in status:
                self.logger.info("Cloud Object Storage:")
                self.logger.info(f"  Valid: {status['cos']['valid']}")
                self.logger.info(f"  Message: {status['cos']['message']}")
            
            if 'error' in status:
                self.logger.error(f"Validation Error: {status['error']}")

        except Exception as e:
            self.logger.error(f"Error logging validation results: {str(e)}")

def main():
    """Main function to run validation."""
    try:
        print("=== IBM Credentials Validation ===")
        validator = IBMCredentialsValidator()
        status = validator.validate_all()
        
        if 'error' in status:
            print(f"Error: {status['error']}")
            return
        
        print("\nCloud Object Storage:")
        print(f"  Valid: {status['cos']['valid']}")
        print(f"  Message: {status['cos']['message']}")
        
        print("\nCheck ibm_validation.log for detailed results")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
