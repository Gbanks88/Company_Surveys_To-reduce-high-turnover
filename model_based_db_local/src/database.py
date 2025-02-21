from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, Model, UMLModel, Requirement, Metadata

T = TypeVar('T')

class DatabaseService:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_db(self):
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
    
    def get_items(self, db: Session, model: Type[T], skip: int = 0, limit: int = 100) -> List[T]:
        """Get multiple items"""
        return db.query(model).offset(skip).limit(limit).all()
    
    def update_item(self, db: Session, model: Type[T], item_id: str, data: Dict[str, Any]) -> Optional[T]:
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
