#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class IBMToMongoPipeline:
    """Pipeline to transfer IBM Cloud service data to MongoDB for AI learning."""
    
    def __init__(self):
        """Initialize the pipeline with configuration."""
        load_dotenv()
        
        # MongoDB connection
        self.mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('MONGODB_DB', 'survey_analytics')
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        
        # IBM Cloud credentials
        self.cos_endpoint = os.getenv('IBM_COS_ENDPOINT').strip("'").strip('"')
        self.cos_api_key = os.getenv('IBM_COS_API_KEY').strip("'").strip('"')
        self.cos_bucket = os.getenv('IBM_COS_BUCKET_NAME').strip("'").strip('"')
        
        # Collections
        self.raw_data_collection = self.db['raw_survey_data']
        self.processed_collection = self.db['processed_data']
        self.model_artifacts_collection = self.db['model_artifacts']
        self.metadata_collection = self.db['metadata']
    
    def _get_iam_token(self) -> str:
        """Get IBM Cloud IAM token."""
        token_url = "https://iam.cloud.ibm.com/identity/token"
        response = requests.post(
            token_url,
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.cos_api_key
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get IAM token: {response.text}")
        
        return response.json()['access_token']
    
    def store_cos_data(self, object_key: str, metadata: Dict[str, Any] = None) -> str:
        """Store data from COS to MongoDB with metadata."""
        try:
            # Get object from COS
            token = self._get_iam_token()
            url = f"{self.cos_endpoint}/{self.cos_bucket}/{object_key}"
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get object from COS: {response.text}")
            
            # Prepare document
            document = {
                "source": "ibm_cos",
                "object_key": object_key,
                "timestamp": datetime.utcnow(),
                "data": response.json() if response.headers.get('content-type') == 'application/json' else response.text,
                "metadata": metadata or {}
            }
            
            # Store in MongoDB
            result = self.raw_data_collection.insert_one(document)
            
            # Log metadata
            self.metadata_collection.insert_one({
                "document_id": result.inserted_id,
                "source": "ibm_cos",
                "object_key": object_key,
                "timestamp": datetime.utcnow(),
                "metadata": metadata or {}
            })
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error storing COS data: {str(e)}")
            raise
    
    def store_processed_data(self, data: Dict[str, Any], source_id: str = None, 
                           model_info: Dict[str, Any] = None) -> str:
        """Store processed data with model information."""
        try:
            document = {
                "data": data,
                "source_id": source_id,
                "model_info": model_info or {},
                "timestamp": datetime.utcnow()
            }
            
            result = self.processed_collection.insert_one(document)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error storing processed data: {str(e)}")
            raise
    
    def store_model_artifact(self, model_name: str, artifact_data: Dict[str, Any], 
                           metadata: Dict[str, Any] = None) -> str:
        """Store ML model artifacts."""
        try:
            document = {
                "model_name": model_name,
                "artifact_data": artifact_data,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow()
            }
            
            result = self.model_artifacts_collection.insert_one(document)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error storing model artifact: {str(e)}")
            raise
    
    def get_training_data(self, query: Dict[str, Any] = None, 
                         limit: int = 1000) -> List[Dict[str, Any]]:
        """Get training data for AI models."""
        try:
            cursor = self.processed_collection.find(
                query or {},
                limit=limit
            )
            return list(cursor)
            
        except Exception as e:
            print(f"Error getting training data: {str(e)}")
            raise
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()

def test_pipeline():
    """Test the IBM to MongoDB pipeline."""
    try:
        pipeline = IBMToMongoPipeline()
        
        # Test storing test file from earlier
        test_id = pipeline.store_cos_data(
            "test/write_test_2025-02-20T21:53:20.364513.json",
            metadata={"test": True, "purpose": "pipeline_validation"}
        )
        print(f"✓ Successfully stored test data in MongoDB")
        print(f"  Document ID: {test_id}")
        
        # Test storing processed data
        processed_id = pipeline.store_processed_data(
            {"test": "processed_data"},
            source_id=test_id,
            model_info={"model": "test_model", "version": "1.0"}
        )
        print(f"✓ Successfully stored processed data")
        print(f"  Document ID: {processed_id}")
        
        pipeline.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    test_pipeline()
