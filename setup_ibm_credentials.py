#!/usr/bin/env python3
import os
import sys
import webbrowser
from getpass import getpass
import json
import requests
from dotenv import load_dotenv, set_key

class IBMCloudSetup:
    def __init__(self):
        self.env_file = '.env'
        load_dotenv(self.env_file)
        
    def setup_credentials(self):
        """Guide user through IBM Cloud credential setup."""
        print("\n=== IBM Cloud Credentials Setup ===\n")
        
        # Step 1: Check if user has IBM Cloud account
        print("Step 1: IBM Cloud Account")
        print("Do you have an IBM Cloud account?")
        print("1. Yes")
        print("2. No - I need to create one")
        choice = input("Choose (1/2): ")
        
        if choice == "2":
            self._open_signup_page()
            input("\nPress Enter once you've created your account...")
        
        # Step 2: Get API Key
        print("\nStep 2: IBM Cloud API Key")
        print("\nYou'll need to create an API key in the IBM Cloud console:")
        print("1. Go to: https://cloud.ibm.com/iam/apikeys")
        print("2. Click 'Create an IBM Cloud API key'")
        print("3. Name it 'survey-app-key' and create")
        print("4. Copy the API key (you won't be able to see it again!)")
        
        open_console = input("\nWould you like to open the API key page now? (y/n): ")
        if open_console.lower() == 'y':
            webbrowser.open('https://cloud.ibm.com/iam/apikeys')
        
        api_key = getpass("\nEnter your API key: ")
        if api_key:
            self._save_credential('IBM_COS_API_KEY', api_key)
            print("✓ API key saved")
        
        # Step 3: Get COS Instance
        print("\nStep 3: Cloud Object Storage Instance")
        print("\nYou'll need to create or select a Cloud Object Storage instance:")
        print("1. Go to: https://cloud.ibm.com/objectstorage/create")
        print("2. Choose 'Lite' plan (free) or any other plan")
        print("3. Create the service")
        print("4. Copy the Instance ID from the service details")
        
        open_cos = input("\nWould you like to open the COS creation page? (y/n): ")
        if open_cos.lower() == 'y':
            webbrowser.open('https://cloud.ibm.com/objectstorage/create')
        
        instance_id = input("\nEnter your COS Instance ID: ")
        if instance_id:
            self._save_credential('IBM_COS_INSTANCE_ID', instance_id)
            print("✓ Instance ID saved")
        
        # Step 4: Get Endpoint
        print("\nStep 4: COS Endpoint")
        print("\nSelect your endpoint region:")
        endpoints = self._get_endpoints()
        for i, (region, endpoint) in enumerate(endpoints.items(), 1):
            print(f"{i}. {region}")
        
        while True:
            try:
                choice = int(input("\nChoose region number: "))
                if 1 <= choice <= len(endpoints):
                    endpoint = list(endpoints.values())[choice-1]
                    self._save_credential('IBM_COS_ENDPOINT', endpoint)
                    print("✓ Endpoint saved")
                    break
            except ValueError:
                print("Please enter a valid number")
        
        # Step 5: Verify Setup
        print("\nStep 5: Verifying Setup")
        if self._verify_credentials():
            print("\n✓ All credentials have been saved successfully!")
            print("✓ Credentials verified and working")
        else:
            print("\n⚠ Credentials saved but verification failed.")
            print("Please check your credentials and try again.")
        
        print("\nCredentials have been saved to:", os.path.abspath(self.env_file))
    
    def _save_credential(self, key, value):
        """Save a credential to .env file."""
        try:
            set_key(self.env_file, key, value)
        except Exception as e:
            print(f"Error saving {key}: {str(e)}")
    
    def _verify_credentials(self):
        """Verify the saved credentials work."""
        try:
            # Import here to avoid circular import
            from ibm_validator import IBMCredentialsValidator
            validator = IBMCredentialsValidator()
            status = validator.validate_all()
            return status.get('cos', {}).get('valid', False)
        except Exception:
            return False
    
    def _get_endpoints(self):
        """Get available COS endpoints."""
        return {
            "US South (Dallas)": "https://s3.us-south.cloud-object-storage.appdomain.cloud",
            "US East (Washington DC)": "https://s3.us-east.cloud-object-storage.appdomain.cloud",
            "EU Great Britain (London)": "https://s3.eu-gb.cloud-object-storage.appdomain.cloud",
            "EU Germany (Frankfurt)": "https://s3.eu-de.cloud-object-storage.appdomain.cloud",
            "Asia Pacific (Tokyo)": "https://s3.jp-tok.cloud-object-storage.appdomain.cloud",
            "Asia Pacific (Sydney)": "https://s3.au-syd.cloud-object-storage.appdomain.cloud"
        }
    
    def _open_signup_page(self):
        """Open IBM Cloud signup page."""
        signup_url = "https://cloud.ibm.com/registration"
        print(f"\nOpening IBM Cloud registration page: {signup_url}")
        webbrowser.open(signup_url)

def main():
    try:
        setup = IBMCloudSetup()
        setup.setup_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
