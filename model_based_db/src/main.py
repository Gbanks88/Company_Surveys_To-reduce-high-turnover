from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

import database
import uml_service
import requirements_service
import models
import schemas

app = FastAPI(title="Model-Based Requirements Database")

# Initialize services
db_service = database.DatabaseService("sqlite:///./modeldb.sqlite")
uml_service = uml_service.UMLService()
requirements_service = requirements_service.RequirementsService(db_service)

# Dependency
def get_db():
    db = next(db_service.get_db())
    try:
        yield db
    finally:
        db.close()

@app.post("/models/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    """Create a new model"""
    return db_service.create_item(db, models.Model, model.dict())

@app.get("/models/{model_id}", response_model=schemas.ModelWithRelations)
def get_model(model_id: UUID, db: Session = Depends(get_db)):
    """Get a model with all its relations"""
    model_data = db_service.get_model_with_relations(db, model_id)
    if not model_data:
        raise HTTPException(status_code=404, detail="Model not found")
    return model_data

@app.post("/models/{model_id}/uml", response_model=schemas.UMLModel)
def add_uml_diagram(
    model_id: UUID,
    uml_data: schemas.UMLModelCreate,
    db: Session = Depends(get_db)
):
    """Add a UML diagram to a model"""
    uml = db_service.add_uml_diagram(db, model_id, uml_data.dict())
    if not uml:
        raise HTTPException(status_code=404, detail="Model not found")
    return uml

@app.post("/requirements/", response_model=schemas.Requirement)
def create_requirement(
    requirement: schemas.RequirementCreate,
    db: Session = Depends(get_db)
):
    """Create a new requirement"""
    errors = requirements_service.validate_requirement(requirement.dict())
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )
    return requirements_service.create_requirement(db, requirement.dict())

@app.get("/requirements/{requirement_id}/trace", response_model=schemas.RequirementTrace)
def get_requirement_trace(requirement_id: UUID, db: Session = Depends(get_db)):
    """Get requirement traceability information"""
    trace = requirements_service.get_requirement_trace(db, requirement_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return trace

@app.put("/requirements/{requirement_id}/status", response_model=schemas.Requirement)
def update_requirement_status(
    requirement_id: UUID,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update requirement status"""
    requirement = requirements_service.update_requirement_status(
        db,
        requirement_id,
        status_update.status,
        status_update.comment
    )
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return requirement

@app.get("/matrix/", response_model=List[schemas.RequirementMatrix])
def get_requirements_matrix(
    model_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """Get requirements traceability matrix"""
    return requirements_service.generate_requirements_matrix(db, model_id)

@app.post("/uml/class-diagram", response_model=schemas.UMLDiagram)
def generate_class_diagram(diagram_data: schemas.ClassDiagramCreate):
    """Generate a class diagram"""
    content = uml_service.generate_class_diagram(
        diagram_data.classes,
        diagram_data.relationships
    )
    filepath = uml_service.save_diagram(content, f"class_{diagram_data.name}.puml")
    return {"name": diagram_data.name, "type": "class", "content": content, "filepath": filepath}

@app.post("/uml/sequence-diagram", response_model=schemas.UMLDiagram)
def generate_sequence_diagram(diagram_data: schemas.SequenceDiagramCreate):
    """Generate a sequence diagram"""
    content = uml_service.generate_sequence_diagram(
        diagram_data.participants,
        diagram_data.messages
    )
    filepath = uml_service.save_diagram(content, f"sequence_{diagram_data.name}.puml")
    return {"name": diagram_data.name, "type": "sequence", "content": content, "filepath": filepath}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
