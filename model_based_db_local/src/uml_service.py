import os
from typing import Optional
import plantuml
import tempfile

class UMLService:
    def __init__(self):
        self.plantuml = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
    
    def generate_diagram(self, diagram_type: str, content: str) -> Optional[str]:
        """Generate a UML diagram from PlantUML content"""
        try:
            # Create temporary file for the diagram
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                # Generate the diagram
                self.plantuml.processes(content, outfile=tmp.name)
                return tmp.name
        except Exception as e:
            print(f"Error generating diagram: {e}")
            return None
    
    def generate_class_diagram(self, classes: list) -> str:
        """Generate PlantUML content for a class diagram"""
        content = ["@startuml"]
        
        for cls in classes:
            content.append(f"class {cls['name']} {{")
            for attr in cls.get('attributes', []):
                content.append(f"  {attr}")
            for method in cls.get('methods', []):
                content.append(f"  {method}")
            content.append("}")
            
            # Add relationships
            for rel in cls.get('relationships', []):
                content.append(f"{cls['name']} {rel['type']} {rel['target']}")
        
        content.append("@enduml")
        return "\n".join(content)
    
    def generate_sequence_diagram(self, sequence: dict) -> str:
        """Generate PlantUML content for a sequence diagram"""
        content = ["@startuml"]
        
        # Add participants
        for participant in sequence.get('participants', []):
            content.append(f"participant {participant}")
        
        # Add messages
        for message in sequence.get('messages', []):
            content.append(f"{message['from']} -> {message['to']}: {message['text']}")
            if message.get('return'):
                content.append(f"{message['to']} --> {message['from']}: {message['return']}")
        
        content.append("@enduml")
        return "\n".join(content)
