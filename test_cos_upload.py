#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

def get_iam_token(api_key):
    """Get IBM Cloud IAM token using API key."""
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
        raise Exception(f"Failed to get IAM token: {token_response.text}")
    
    return token_response.json()['access_token']

def upload_test_file():
    """Upload a test file to IBM Cloud Object Storage."""
    load_dotenv()
    
    # Get credentials
    endpoint = os.getenv('IBM_COS_ENDPOINT').strip("'").strip('"')
    api_key = os.getenv('IBM_COS_API_KEY').strip("'").strip('"')
    bucket = os.getenv('IBM_COS_BUCKET_NAME').strip("'").strip('"')
    
    try:
        # Get IAM token
        access_token = get_iam_token(api_key)
        
        # Create test content
        timestamp = datetime.now().isoformat()
        test_content = {
            'test_id': 'cos_write_test',
            'timestamp': timestamp,
            'status': 'testing write permissions'
        }
        
        # Upload test file
        test_key = f'test/write_test_{timestamp}.json'
        upload_url = f"{endpoint}/{bucket}/{test_key}"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.put(
            upload_url,
            headers=headers,
            data=json.dumps(test_content)
        )
        
        if response.status_code == 200:
            print(f"✓ Successfully uploaded test file")
            print(f"  Bucket: {bucket}")
            print(f"  File: {test_key}")
            return True
        else:
            print(f"✗ Failed to upload test file")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error during upload test: {str(e)}")
        return False

if __name__ == "__main__":
    upload_test_file()
