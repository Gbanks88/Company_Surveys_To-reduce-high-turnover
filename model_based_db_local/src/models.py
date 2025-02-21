from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.dialects.sqlite import UUID
import uuid

class Base(DeclarativeBase):
    pass

# Association tables
model_requirement = Table(
    'model_requirement',
    Base.metadata,
    Column('model_id', UUID, ForeignKey('models.id')),
    Column('requirement_id', UUID, ForeignKey('requirements.id'))
)

class Model(Base):
    __tablename__ = "models"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    uml_diagrams = relationship("UMLModel", back_populates="model")
    requirements = relationship("Requirement", secondary=model_requirement, back_populates="models")
    metadata = relationship("Metadata", back_populates="model")

class UMLModel(Base):
    __tablename__ = "uml_diagrams"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID, ForeignKey("models.id"))
    diagram_type = Column(String, nullable=False)  # class, sequence, component, etc.
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    model = relationship("Model", back_populates="uml_diagrams")

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="new")  # new, in_progress, completed, etc.
    priority = Column(String, default="medium")  # low, medium, high
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    models = relationship("Model", secondary=model_requirement, back_populates="requirements")
    metadata = relationship("Metadata", back_populates="requirement")

class Metadata(Base):
    __tablename__ = "metadata"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID, ForeignKey("models.id"), nullable=True)
    requirement_id = Column(UUID, ForeignKey("requirements.id"), nullable=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    model = relationship("Model", back_populates="metadata")
    requirement = relationship("Requirement", back_populates="metadata")
