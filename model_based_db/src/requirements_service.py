from typing import Dict, List, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session
from .database import DatabaseService
from .models import Requirement, Model, UMLModel

class RequirementsService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def create_requirement(
        self,
        db: Session,
        requirement_data: Dict,
        parent_id: Optional[UUID] = None,
        model_ids: Optional[List[UUID]] = None
    ) -> Requirement:
        """Create a new requirement"""
        requirement_data['parent_id'] = parent_id
        requirement = self.db_service.create_item(db, Requirement, requirement_data)
        
        if model_ids:
            for model_id in model_ids:
                model = self.db_service.get_item(db, Model, model_id)
                if model:
                    model.requirements.append(requirement)
        
        db.commit()
        db.refresh(requirement)
        return requirement
    
    def update_requirement_status(
        self,
        db: Session,
        requirement_id: UUID,
        new_status: str,
        comment: Optional[str] = None
    ) -> Optional[Requirement]:
        """Update requirement status with optional comment"""
        requirement = self.db_service.get_item(db, Requirement, requirement_id)
        if requirement:
            metadata = requirement.metadata or {}
            status_history = metadata.get('status_history', [])
            status_history.append({
                'status': new_status,
                'timestamp': datetime.utcnow().isoformat(),
                'comment': comment
            })
            metadata['status_history'] = status_history
            
            return self.db_service.update_item(
                db,
                Requirement,
                requirement_id,
                {
                    'status': new_status,
                    'metadata': metadata
                }
            )
        return None
    
    def get_requirement_trace(
        self,
        db: Session,
        requirement_id: UUID
    ) -> Dict:
        """Get requirement traceability information"""
        requirement = self.db_service.get_item(db, Requirement, requirement_id)
        if not requirement:
            return {}
        
        trace = {
            'requirement': requirement,
            'parent': None,
            'children': [],
            'models': [],
            'related_uml': []
        }
        
        # Get parent
        if requirement.parent_id:
            trace['parent'] = self.db_service.get_item(
                db, Requirement, requirement.parent_id
            )
        
        # Get children
        trace['children'] = requirement.children
        
        # Get associated models
        trace['models'] = requirement.models
        
        # Get related UML diagrams
        for model in requirement.models:
            trace['related_uml'].extend(model.uml_diagrams)
        
        return trace
    
    def validate_requirement(self, requirement_data: Dict) -> List[str]:
        """Validate requirement data"""
        errors = []
        
        # Required fields
        required_fields = ['name', 'type', 'priority', 'status']
        for field in required_fields:
            if field not in requirement_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate type
        valid_types = ['functional', 'non-functional', 'technical', 'business']
        if requirement_data.get('type') not in valid_types:
            errors.append(f"Invalid requirement type. Must be one of: {valid_types}")
        
        # Validate priority
        valid_priorities = ['high', 'medium', 'low']
        if requirement_data.get('priority') not in valid_priorities:
            errors.append(f"Invalid priority. Must be one of: {valid_priorities}")
        
        # Validate status
        valid_statuses = ['draft', 'approved', 'implemented', 'verified', 'rejected']
        if requirement_data.get('status') not in valid_statuses:
            errors.append(f"Invalid status. Must be one of: {valid_statuses}")
        
        # Validate acceptance criteria
        if 'acceptance_criteria' in requirement_data:
            criteria = requirement_data['acceptance_criteria']
            if not isinstance(criteria, str) or len(criteria.strip()) < 10:
                errors.append("Acceptance criteria must be a string with at least 10 characters")
        
        return errors
    
    def generate_requirements_matrix(
        self,
        db: Session,
        model_id: Optional[UUID] = None
    ) -> List[Dict]:
        """Generate requirements traceability matrix"""
        query = db.query(Requirement)
        if model_id:
            query = query.join(Requirement.models).filter(Model.id == model_id)
        
        requirements = query.all()
        matrix = []
        
        for req in requirements:
            trace = self.get_requirement_trace(db, req.id)
            matrix.append({
                'id': req.id,
                'name': req.name,
                'type': req.type,
                'status': req.status,
                'parent': trace['parent'].name if trace['parent'] else None,
                'children': [child.name for child in trace['children']],
                'models': [model.name for model in trace['models']],
                'uml_diagrams': [uml.name for uml in trace['related_uml']]
            })
        
        return matrix
