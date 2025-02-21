#!/usr/bin/env python3
import os
import json
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv
from ibm_to_mongo_pipeline import IBMToMongoPipeline
import xml.etree.ElementTree as ET
from datetime import datetime

class IBMModelGenerator:
    """IBM-powered Model-Based Software Engineering system."""
    
    def __init__(self):
        """Initialize the model generator."""
        load_dotenv()
        self.pipeline = IBMToMongoPipeline()
        
        # IBM Watson credentials
        self.nlu_api_key = os.getenv('IBM_WATSON_NLU_API_KEY')
        self.nlu_url = os.getenv('IBM_WATSON_NLU_URL')
        self.nlu_version = os.getenv('IBM_WATSON_NLU_VERSION')
        
        # Collections for model storage
        self.models_collection = self.pipeline.db['software_models']
        self.diagrams_collection = self.pipeline.db['uml_diagrams']
        self.relationships_collection = self.pipeline.db['model_relationships']
    
    def analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """Analyze code structure using Watson NLU."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._get_nlu_token()}'
            }
            
            # Use NLU to analyze code structure and relationships
            payload = {
                'text': code,
                'features': {
                    'entities': {
                        'model': 'code-analysis-v1',
                        'sentiment': False,
                        'limit': 50
                    },
                    'relations': {
                        'model': 'code-analysis-v1'
                    },
                    'syntax': {
                        'tokens': {
                            'lemma': True,
                            'part_of_speech': True
                        }
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
                raise Exception(f"Code analysis failed: {response.text}")
            
            return response.json()
            
        except Exception as e:
            print(f"Error analyzing code: {str(e)}")
            raise
    
    def generate_uml_from_code(self, code: str, diagram_type: str = 'class') -> str:
        """Generate UML diagram from code analysis."""
        try:
            # Analyze code structure
            analysis = self.analyze_code_structure(code)
            
            # Extract entities (classes, interfaces, methods)
            entities = analysis.get('entities', [])
            relations = analysis.get('relations', [])
            
            # Create DrawIO XML structure
            diagram = self._create_drawio_diagram()
            
            # Add entities to diagram
            entity_elements = {}
            y_position = 40
            for entity in entities:
                if entity['type'] in ['Class', 'Interface', 'Method']:
                    element = self._create_entity_element(
                        entity['text'],
                        entity['type'],
                        x=240,
                        y=y_position
                    )
                    diagram.append(element)
                    entity_elements[entity['text']] = element
                    y_position += 100
            
            # Add relationships
            for relation in relations:
                if relation['type'] in ['inherits', 'implements', 'uses']:
                    source = entity_elements.get(relation['source']['text'])
                    target = entity_elements.get(relation['target']['text'])
                    if source is not None and target is not None:
                        connection = self._create_relationship(
                            source.get('id'),
                            target.get('id'),
                            relation['type']
                        )
                        diagram.append(connection)
            
            # Save diagram to MongoDB
            diagram_id = self.diagrams_collection.insert_one({
                'type': diagram_type,
                'content': ET.tostring(diagram, encoding='unicode'),
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'entities_count': len(entities),
                    'relationships_count': len(relations)
                }
            }).inserted_id
            
            return str(diagram_id)
            
        except Exception as e:
            print(f"Error generating UML: {str(e)}")
            raise
    
    def _create_drawio_diagram(self) -> ET.Element:
        """Create base DrawIO diagram structure."""
        mxfile = ET.Element('mxfile')
        diagram = ET.SubElement(mxfile, 'diagram')
        mxGraphModel = ET.SubElement(diagram, 'mxGraphModel')
        root = ET.SubElement(mxGraphModel, 'root')
        
        # Add default parent
        parent = ET.SubElement(root, 'mxCell', id='0')
        parent = ET.SubElement(root, 'mxCell', id='1', parent='0')
        
        return root
    
    def _create_entity_element(self, name: str, entity_type: str, x: int, y: int) -> ET.Element:
        """Create an entity element (class, interface, etc.)."""
        entity_id = f"entity_{name.replace(' ', '_')}"
        
        cell = ET.Element('mxCell', {
            'id': entity_id,
            'value': f"&lt;p&gt;{entity_type}&lt;/p&gt;&lt;p&gt;{name}&lt;/p&gt;",
            'vertex': '1',
            'parent': '1'
        })
        
        geometry = ET.SubElement(cell, 'mxGeometry', {
            'x': str(x),
            'y': str(y),
            'width': '160',
            'height': '80',
            'as': 'geometry'
        })
        
        return cell
    
    def _create_relationship(self, source_id: str, target_id: str, relation_type: str) -> ET.Element:
        """Create a relationship connection."""
        edge_id = f"edge_{source_id}_{target_id}"
        
        edge_style = {
            'inherits': 'endArrow=block;endSize=16;endFill=0;',
            'implements': 'endArrow=block;endSize=16;endFill=0;dashed=1;',
            'uses': 'endArrow=open;endSize=12;'
        }
        
        cell = ET.Element('mxCell', {
            'id': edge_id,
            'edge': '1',
            'parent': '1',
            'source': source_id,
            'target': target_id,
            'style': edge_style.get(relation_type, 'endArrow=none;')
        })
        
        geometry = ET.SubElement(cell, 'mxGeometry', {
            'relative': '1',
            'as': 'geometry'
        })
        
        return cell
    
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

def test_model_generator():
    """Test the model generator with sample code."""
    try:
        generator = IBMModelGenerator()
        
        # Sample code for testing
        test_code = """
        class Employee:
            def __init__(self, name, position):
                self.name = name
                self.position = position
            
            def get_details(self):
                return f"{self.name} - {self.position}"
        
        class Manager(Employee):
            def __init__(self, name, department):
                super().__init__(name, "Manager")
                self.department = department
            
            def get_team(self):
                return f"Team: {self.department}"
        
        class Developer(Employee):
            def __init__(self, name, language):
                super().__init__(name, "Developer")
                self.language = language
            
            def get_skills(self):
                return f"Skills: {self.language}"
        """
        
        # Generate UML diagram
        diagram_id = generator.generate_uml_from_code(test_code)
        print(f"✓ Successfully generated UML diagram")
        print(f"  Diagram ID: {diagram_id}")
        
        generator.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing model generator: {str(e)}")
        return False

if __name__ == "__main__":
    test_model_generator()
