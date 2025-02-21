import os
from typing import Dict, List, Optional
import plantuml
from graphviz import Digraph

class UMLService:
    def __init__(self, output_dir: str = "models/uml"):
        self.output_dir = output_dir
        self.plantuml = plantuml.PlantUML()
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_class_diagram(
        self,
        classes: List[Dict[str, any]],
        relationships: List[Dict[str, any]]
    ) -> str:
        """Generate PlantUML class diagram"""
        uml = ["@startuml"]
        
        # Add classes
        for cls in classes:
            uml.append(f"class {cls['name']} {{")
            if 'attributes' in cls:
                for attr in cls['attributes']:
                    uml.append(f"  {attr['visibility']} {attr['name']}: {attr['type']}")
            if 'methods' in cls:
                for method in cls['methods']:
                    params = ", ".join([f"{p['name']}: {p['type']}" for p in method.get('parameters', [])])
                    uml.append(f"  {method['visibility']} {method['name']}({params}): {method['return_type']}")
            uml.append("}")
        
        # Add relationships
        for rel in relationships:
            uml.append(f"{rel['from']} {rel['type']} {rel['to']}")
        
        uml.append("@enduml")
        return "\n".join(uml)
    
    def generate_sequence_diagram(
        self,
        participants: List[str],
        messages: List[Dict[str, any]]
    ) -> str:
        """Generate PlantUML sequence diagram"""
        uml = ["@startuml"]
        
        # Add participants
        for participant in participants:
            uml.append(f"participant {participant}")
        
        # Add messages
        for msg in messages:
            if msg.get('type') == 'activation':
                uml.append(f"activate {msg['participant']}")
            elif msg.get('type') == 'deactivation':
                uml.append(f"deactivate {msg['participant']}")
            else:
                uml.append(f"{msg['from']} -> {msg['to']}: {msg['message']}")
        
        uml.append("@enduml")
        return "\n".join(uml)
    
    def generate_component_diagram(
        self,
        components: List[Dict[str, any]],
        interfaces: List[Dict[str, any]],
        dependencies: List[Dict[str, any]]
    ) -> str:
        """Generate PlantUML component diagram"""
        uml = ["@startuml"]
        
        # Add components
        for comp in components:
            uml.append(f"[{comp['name']}] as {comp['id']}")
        
        # Add interfaces
        for iface in interfaces:
            uml.append(f"interface {iface['name']} as {iface['id']}")
        
        # Add dependencies
        for dep in dependencies:
            uml.append(f"{dep['from']} --> {dep['to']}")
        
        uml.append("@enduml")
        return "\n".join(uml)
    
    def generate_state_diagram(
        self,
        states: List[Dict[str, any]],
        transitions: List[Dict[str, any]]
    ) -> str:
        """Generate PlantUML state diagram"""
        uml = ["@startuml"]
        
        # Add states
        for state in states:
            if state.get('type') == 'start':
                uml.append("[*] --> " + state['name'])
            elif state.get('type') == 'end':
                uml.append(state['name'] + " --> [*]")
            else:
                uml.append(f"state {state['name']}")
        
        # Add transitions
        for trans in transitions:
            uml.append(f"{trans['from']} --> {trans['to']}: {trans.get('label', '')}")
        
        uml.append("@enduml")
        return "\n".join(uml)
    
    def save_diagram(self, content: str, filename: str) -> str:
        """Save UML diagram to file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def generate_requirement_diagram(
        self,
        requirements: List[Dict[str, any]],
        relationships: List[Dict[str, any]]
    ) -> str:
        """Generate requirement diagram using Graphviz"""
        dot = Digraph(comment='Requirements Diagram')
        dot.attr(rankdir='TB')
        
        # Add requirements
        for req in requirements:
            label = f"{req['id']}\n{req['name']}\n{req['type']}"
            dot.node(req['id'], label, shape='box')
        
        # Add relationships
        for rel in relationships:
            dot.edge(rel['from'], rel['to'], rel.get('type', ''))
        
        return dot.source
