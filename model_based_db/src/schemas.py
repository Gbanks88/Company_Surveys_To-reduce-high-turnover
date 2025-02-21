from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

# Base schemas
class BaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# UML schemas
class UMLModelBase(BaseSchema):
    diagram_type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class UMLModelCreate(UMLModelBase):
    pass

class UMLModel(UMLModelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_id: UUID

# Requirement schemas
class RequirementBase(BaseSchema):
    type: str
    priority: str
    status: str
    acceptance_criteria: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RequirementCreate(RequirementBase):
    parent_id: Optional[UUID] = None
    model_ids: Optional[List[UUID]] = None

class Requirement(RequirementBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    parent_id: Optional[UUID] = None

class RequirementTrace(BaseModel):
    requirement: Requirement
    parent: Optional[Requirement]
    children: List[Requirement]
    models: List['Model']
    related_uml: List[UMLModel]

# Model schemas
class ModelBase(BaseSchema):
    type: str
    version: str
    status: str
    metadata: Optional[Dict[str, Any]] = None

class ModelCreate(ModelBase):
    pass

class Model(ModelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    parent_id: Optional[UUID] = None

class ModelWithRelations(Model):
    requirements: List[Requirement]
    uml_diagrams: List[UMLModel]
    children: List[Model]

# Status update schema
class StatusUpdate(BaseModel):
    status: str
    comment: Optional[str] = None

# Requirements matrix schema
class RequirementMatrix(BaseModel):
    id: UUID
    name: str
    type: str
    status: str
    parent: Optional[str]
    children: List[str]
    models: List[str]
    uml_diagrams: List[str]

# UML diagram creation schemas
class ClassAttribute(BaseModel):
    name: str
    type: str
    visibility: str = "public"

class MethodParameter(BaseModel):
    name: str
    type: str

class ClassMethod(BaseModel):
    name: str
    return_type: str
    visibility: str = "public"
    parameters: Optional[List[MethodParameter]] = None

class ClassDefinition(BaseModel):
    name: str
    attributes: Optional[List[ClassAttribute]] = None
    methods: Optional[List[ClassMethod]] = None

class Relationship(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    type: str  # inheritance, composition, aggregation, association

class ClassDiagramCreate(BaseModel):
    name: str
    classes: List[ClassDefinition]
    relationships: List[Relationship]

class Message(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    message: str
    type: Optional[str] = None  # normal, activation, deactivation

class SequenceDiagramCreate(BaseModel):
    name: str
    participants: List[str]
    messages: List[Message]

class UMLDiagram(BaseModel):
    name: str
    type: str
    content: str
    filepath: str

# Update forward references
RequirementTrace.update_forward_refs(Model=Model)
