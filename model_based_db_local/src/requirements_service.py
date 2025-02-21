from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from database import DatabaseService
from models import Requirement, Model, Metadata

class RequirementsService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def create_requirement(self, db: Session, requirement_data: dict) -> Requirement:
        """Create a new requirement"""
        return self.db_service.create_item(db, Requirement, requirement_data)
    
    def get_requirement(self, db: Session, requirement_id: str) -> Optional[Requirement]:
        """Get a requirement by ID"""
        return self.db_service.get_item(db, Requirement, requirement_id)
    
    def get_requirements(self, db: Session, skip: int = 0, limit: int = 100) -> List[Requirement]:
        """Get multiple requirements"""
        return self.db_service.get_items(db, Requirement, skip, limit)
    
    def update_requirement(self, db: Session, requirement_id: str, requirement_data: dict) -> Optional[Requirement]:
        """Update a requirement"""
        return self.db_service.update_item(db, Requirement, requirement_id, requirement_data)
    
    def delete_requirement(self, db: Session, requirement_id: str) -> bool:
        """Delete a requirement"""
        return self.db_service.delete_item(db, Requirement, requirement_id)
    
    def add_metadata(self, db: Session, requirement_id: str, metadata: Dict[str, str]) -> List[Metadata]:
        """Add metadata to a requirement"""
        requirement = self.get_requirement(db, requirement_id)
        if not requirement:
            return []
        
        metadata_items = []
        for key, value in metadata.items():
            metadata_item = Metadata(
                requirement_id=requirement_id,
                key=key,
                value=value
            )
            db.add(metadata_item)
            metadata_items.append(metadata_item)
        
        db.commit()
        return metadata_items
    
    def get_traceability_matrix(self, db: Session, model_id: Optional[str] = None) -> List[Dict]:
        """Generate a traceability matrix"""
        query = db.query(Requirement, Model)
        if model_id:
            query = query.filter(Model.id == model_id)
        
        matrix = []
        for req, model in query.all():
            matrix.append({
                'requirement_id': str(req.id),
                'requirement_title': req.title,
                'model_id': str(model.id),
                'model_name': model.name
            })
        
        return matrix
