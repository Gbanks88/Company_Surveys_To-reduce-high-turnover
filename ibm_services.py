#!/usr/bin/env python3
import os
import json
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv
from ibm_to_mongo_pipeline import IBMToMongoPipeline

class IBMServicesManager:
    """Manager for IBM Cloud services integration."""
    
    def __init__(self):
        """Initialize IBM services manager."""
        load_dotenv()
        self.pipeline = IBMToMongoPipeline()
        
        # Watson NLU credentials
        self.nlu_api_key = os.getenv('IBM_WATSON_NLU_API_KEY')
        self.nlu_url = os.getenv('IBM_WATSON_NLU_URL')
        self.nlu_version = os.getenv('IBM_WATSON_NLU_VERSION')
    
    def analyze_survey_response(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Analyze survey response using Watson NLU."""
        try:
            # Call Watson NLU
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._get_nlu_token()}'
            }
            
            payload = {
                'text': text,
                'features': {
                    'sentiment': {},
                    'keywords': {
                        'limit': 10
                    },
                    'emotion': {},
                    'categories': {
                        'limit': 3
                    }
                },
                'language': 'en'
            }
            
            response = requests.post(
                f"{self.nlu_url}/v1/analyze?version={self.nlu_version}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"NLU analysis failed: {response.text}")
            
            analysis_result = response.json()
            
            # Store raw NLU response
            raw_id = self.pipeline.store_cos_data(
                f"nlu_analysis/{metadata.get('survey_id', 'unknown')}.json",
                metadata={
                    'analysis_type': 'nlu',
                    'survey_metadata': metadata
                }
            )
            
            # Process and store results
            processed_data = {
                'text': text,
                'sentiment': analysis_result.get('sentiment', {}).get('document', {}),
                'keywords': analysis_result.get('keywords', []),
                'emotions': analysis_result.get('emotion', {}).get('document', {}).get('emotion', {}),
                'categories': analysis_result.get('categories', []),
                'metadata': metadata or {}
            }
            
            processed_id = self.pipeline.store_processed_data(
                processed_data,
                source_id=raw_id,
                model_info={
                    'type': 'sentiment_analysis',
                    'service': 'watson_nlu',
                    'version': self.nlu_version
                }
            )
            
            return processed_id
            
        except Exception as e:
            print(f"Error analyzing survey response: {str(e)}")
            raise
    
    def analyze_batch_responses(self, responses: List[Dict[str, Any]]) -> List[str]:
        """Analyze multiple survey responses."""
        results = []
        for response in responses:
            try:
                processed_id = self.analyze_survey_response(
                    response['text'],
                    metadata=response.get('metadata', {})
                )
                results.append(processed_id)
            except Exception as e:
                print(f"Error processing response: {str(e)}")
                continue
        return results
    
    def _get_nlu_token(self) -> str:
        """Get Watson NLU authentication token."""
        try:
            response = requests.post(
                'https://iam.cloud.ibm.com/identity/token',
                data={
                    'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                    'apikey': self.nlu_api_key
                },
                headers={'Accept': 'application/json'}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get NLU token: {response.text}")
            
            return response.json()['access_token']
            
        except Exception as e:
            print(f"Error getting NLU token: {str(e)}")
            raise
    
    def close(self):
        """Close connections."""
        self.pipeline.close()

def test_services():
    """Test IBM services integration."""
    try:
        services = IBMServicesManager()
        
        # Test survey responses
        test_responses = [
            {
                'text': 'I really enjoy working with my team. The projects are challenging but rewarding.',
                'metadata': {
                    'department': 'Engineering',
                    'survey_id': 'eng_2025_q1_001'
                }
            },
            {
                'text': 'Management could improve communication about company goals and direction.',
                'metadata': {
                    'department': 'Marketing',
                    'survey_id': 'mkt_2025_q1_002'
                }
            }
        ]
        
        # Process responses
        result_ids = services.analyze_batch_responses(test_responses)
        
        print(f"✓ Successfully analyzed {len(result_ids)} responses")
        for i, id in enumerate(result_ids):
            print(f"  Response {i+1} ID: {id}")
        
        services.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing services: {str(e)}")
        return False

if __name__ == "__main__":
    test_services()
