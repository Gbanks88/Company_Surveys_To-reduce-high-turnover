from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import DeclarativeMeta

import models
from models import Base, Model, UMLModel, Requirement, Metadata

T = TypeVar('T')

class DatabaseService:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_database(self) -> None:
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_db(self) -> Session:
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_item(self, db: Session, model: Type[T], data: Dict[str, Any]) -> T:
        """Create a new item"""
        db_item = model(**data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def get_item(self, db: Session, model: Type[T], item_id: str) -> Optional[T]:
        """Get an item by ID"""
        return db.query(model).filter(model.id == item_id).first()
    
    def get_items(
        self, 
        db: Session, 
        model: Type[T], 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """Get multiple items with optional filtering"""
        query = db.query(model)
        if filters:
            for key, value in filters.items():
                if hasattr(model, key):
                    query = query.filter(getattr(model, key) == value)
        return query.offset(skip).limit(limit).all()
    
    def update_item(
        self, 
        db: Session, 
        model: Type[T], 
        item_id: str, 
        data: Dict[str, Any]
    ) -> Optional[T]:
        """Update an item"""
        db_item = self.get_item(db, model, item_id)
        if db_item:
            for key, value in data.items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
        return db_item
    
    def delete_item(self, db: Session, model: Type[T], item_id: str) -> bool:
        """Delete an item"""
        db_item = self.get_item(db, model, item_id)
        if db_item:
            db.delete(db_item)
            db.commit()
            return True
        return False
    
    # Model-specific methods
    def create_model_with_requirements(
        self,
        db: Session,
        model_data: Dict[str, Any],
        requirements: List[Dict[str, Any]]
    ) -> Model:
        """Create a model with associated requirements"""
        model = self.create_item(db, Model, model_data)
        for req_data in requirements:
            requirement = self.create_item(db, Requirement, req_data)
            model.requirements.append(requirement)
        db.commit()
        db.refresh(model)
        return model
    
    def add_uml_diagram(
        self,
        db: Session,
        model_id: str,
        uml_data: Dict[str, Any]
    ) -> Optional[UMLModel]:
        """Add a UML diagram to a model"""
        model = self.get_item(db, Model, model_id)
        if model:
            uml_diagram = self.create_item(db, UMLModel, {**uml_data, "model_id": model_id})
            return uml_diagram
        return None
    
    def get_model_with_relations(
        self,
        db: Session,
        model_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a model with all its relations"""
        model = self.get_item(db, Model, model_id)
        if model:
            return {
                "model": model,
                "requirements": model.requirements,
                "uml_diagrams": model.uml_diagrams,
                "children": model.children
            }
        return None
