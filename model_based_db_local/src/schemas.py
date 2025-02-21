from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None

class ModelCreate(ModelBase):
    pass

class Model(ModelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UMLModelBase(BaseModel):
    diagram_type: str
    content: str

class UMLModelCreate(UMLModelBase):
    model_id: UUID

class UMLModel(UMLModelBase):
    id: UUID
    model_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RequirementBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "new"
    priority: Optional[str] = "medium"

class RequirementCreate(RequirementBase):
    pass

class Requirement(RequirementBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MetadataBase(BaseModel):
    key: str
    value: str

class MetadataCreate(MetadataBase):
    model_id: Optional[UUID] = None
    requirement_id: Optional[UUID] = None

class Metadata(MetadataBase):
    id: UUID
    model_id: Optional[UUID]
    requirement_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClassDiagramCreate(BaseModel):
    classes: List[Dict]

class SequenceDiagramCreate(BaseModel):
    participants: List[str]
    messages: List[Dict]
