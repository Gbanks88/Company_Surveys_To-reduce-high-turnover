#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from requirements_manager import (
    RequirementsManager, RequirementType, 
    RequirementStatus, UseCaseStatus
)

app = FastAPI(title="Requirements Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for validation
class RequirementCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    type: RequirementType
    priority: int = Field(..., ge=1, le=5)
    acceptance_criteria: List[str] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('title')
    @classmethod
    def title_must_be_descriptive(cls, v):
        if len(v.split()) < 3:
            raise ValueError('Title must be at least 3 words')
        return v

    @field_validator('description')
    @classmethod
    def description_must_be_detailed(cls, v):
        if len(v.split()) < 10:
            raise ValueError('Description must be at least 10 words')
        return v

    @field_validator('acceptance_criteria')
    @classmethod
    def validate_acceptance_criteria(cls, v):
        if not v:
            raise ValueError('At least one acceptance criterion is required')
        for criterion in v:
            if len(criterion.split()) < 3:
                raise ValueError('Each criterion must be at least 3 words')
        return v

class UseCaseCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    actor: str = Field(..., min_length=2)
    preconditions: List[str] = Field(default_factory=list)
    postconditions: List[str] = Field(default_factory=list)
    main_flow: List[str] = Field(...)
    alternative_flows: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    priority: int = Field(..., ge=1, le=5)

    @field_validator('main_flow')
    @classmethod
    def validate_main_flow(cls, v):
        if not v:
            raise ValueError('Main flow must have at least one step')
        for step in v:
            if not step.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                raise ValueError('Each step must start with a number followed by a period')
        return v

# Dependency to get RequirementsManager instance
def get_requirements_manager():
    manager = RequirementsManager()
    try:
        yield manager
    finally:
        manager.close()

# API Routes
@app.post("/requirements/", response_model=dict)
async def create_requirement(
    requirement: RequirementCreate,
    manager: RequirementsManager = Depends(get_requirements_manager)
):
    """Create a new requirement with validation."""
    try:
        req_id = manager.create_requirement(requirement.model_dump())
        return {"id": req_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/use-cases/", response_model=dict)
async def create_use_case(
    use_case: UseCaseCreate,
    manager: RequirementsManager = Depends(get_requirements_manager)
):
    """Create a new use case with validation."""
    try:
        uc_id = manager.create_use_case(use_case.model_dump())
        return {"id": uc_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/requirements/{req_id}/trace")
async def get_requirement_trace(
    req_id: str,
    manager: RequirementsManager = Depends(get_requirements_manager)
):
    """Get requirement traceability matrix."""
    try:
        trace = manager.get_requirement_trace(req_id)
        return trace
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/requirements/")
async def list_requirements(
    status: Optional[RequirementStatus] = None,
    type: Optional[RequirementType] = None,
    priority: Optional[int] = None,
    manager: RequirementsManager = Depends(get_requirements_manager)
):
    """List requirements with optional filters."""
    try:
        query = {}
        if status:
            query["status"] = status.value
        if type:
            query["type"] = type.value
        if priority:
            query["priority"] = priority
        
        requirements = list(manager.requirements.find(query))
        return {"requirements": requirements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/use-cases/")
async def list_use_cases(
    status: Optional[UseCaseStatus] = None,
    priority: Optional[int] = None,
    manager: RequirementsManager = Depends(get_requirements_manager)
):
    """List use cases with optional filters."""
    try:
        query = {}
        if status:
            query["status"] = status.value
        if priority:
            query["priority"] = priority
        
        use_cases = list(manager.use_cases.find(query))
        return {"use_cases": use_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
