from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PSQL_UUID

Base = declarative_base()

# Association tables
model_requirement = Table(
    'model_requirement',
    Base.metadata,
    Column('model_id', PSQL_UUID(as_uuid=True), ForeignKey('models.id')),
    Column('requirement_id', PSQL_UUID(as_uuid=True), ForeignKey('requirements.id'))
)

class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True
    
    id = Column(PSQL_UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String, nullable=False)
    description = Column(String)

class UMLModel(BaseModel):
    """UML model representation"""
    __tablename__ = 'uml_models'
    
    diagram_type = Column(String, nullable=False)  # class, sequence, activity, etc.
    content = Column(String, nullable=False)  # PlantUML content
    metadata = Column(JSON)
    
    model_id = Column(PSQL_UUID(as_uuid=True), ForeignKey('models.id'))
    model = relationship("Model", back_populates="uml_diagrams")

class Requirement(BaseModel):
    """Requirement representation"""
    __tablename__ = 'requirements'
    
    type = Column(String, nullable=False)  # functional, non-functional, etc.
    priority = Column(String, nullable=False)  # high, medium, low
    status = Column(String, nullable=False)  # draft, approved, implemented, etc.
    acceptance_criteria = Column(String)
    metadata = Column(JSON)
    
    models = relationship("Model", secondary=model_requirement, back_populates="requirements")
    parent_id = Column(PSQL_UUID(as_uuid=True), ForeignKey('requirements.id'))
    children = relationship("Requirement")

class Model(BaseModel):
    """Core model representation"""
    __tablename__ = 'models'
    
    type = Column(String, nullable=False)  # domain, system, component, etc.
    version = Column(String, nullable=False)
    status = Column(String, nullable=False)  # draft, approved, deprecated, etc.
    metadata = Column(JSON)
    
    uml_diagrams = relationship("UMLModel", back_populates="model")
    requirements = relationship("Requirement", secondary=model_requirement, back_populates="models")
    
    parent_id = Column(PSQL_UUID(as_uuid=True), ForeignKey('models.id'))
    children = relationship("Model")

class Metadata(BaseModel):
    """Metadata for models and requirements"""
    __tablename__ = 'metadata'
    
    key = Column(String, nullable=False)
    value = Column(JSON)
    category = Column(String, nullable=False)  # model, requirement, uml, etc.
    
    def __repr__(self):
        return f"<Metadata(key='{self.key}', category='{self.category}')>"
