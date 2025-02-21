import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import sqlite3
import json
import logging
import logging.config
import os

from config import DATABASE, STATIC, LOGGING, VEHICLE, SIMULATION
from vention_integration import MockVentionAPI, VentionMachine, sync_machine_requirements

# Configure logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Model-Based Requirements Management System")

# Create logs directory if it doesn't exist
log_dir = os.path.join(Path(__file__).parent.parent, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC['directory']), name="static")

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE['requirements'])
    try:
        c = conn.cursor()
        
        # Create models table
        c.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Create requirements table
        c.execute('''
            CREATE TABLE IF NOT EXISTS requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT,
                priority TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Create UML diagrams table
        c.execute('''
            CREATE TABLE IF NOT EXISTS uml_diagrams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT,
                model_id INTEGER,
                created_at TIMESTAMP,
                FOREIGN KEY (model_id) REFERENCES models (id)
            )
        ''')
        
        # Create metadata table
        c.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT,
                type TEXT,
                item_id INTEGER,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise
    finally:
        conn.close()

# Initialize database on startup
init_db()

# Initialize Vention API mock
vention_api = MockVentionAPI()

# Pydantic models
class ModelBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    status: Optional[str] = None

class Model(ModelBase):
    id: int
    created_at: datetime
    updated_at: datetime

class RequirementBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class Requirement(RequirementBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UMLDiagramBase(BaseModel):
    title: str
    type: str
    content: str
    model_id: Optional[int] = None

class UMLDiagram(UMLDiagramBase):
    id: int
    created_at: datetime

class MetadataBase(BaseModel):
    key: str
    value: str
    type: Optional[str] = None
    item_id: Optional[int] = None

class Metadata(MetadataBase):
    id: int
    created_at: datetime

class MoveRequest(BaseModel):
    component_id: str
    axis: str
    position: float

class CoordinatedMoveRequest(BaseModel):
    component_id: str
    positions: Dict[str, float]

# WebSocket connections store
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, machine_id: str):
        await websocket.accept()
        if machine_id not in self.active_connections:
            self.active_connections[machine_id] = []
        self.active_connections[machine_id].append(websocket)
        logger.info(f"New WebSocket connection for machine {machine_id}")

    def disconnect(self, websocket: WebSocket, machine_id: str):
        if machine_id in self.active_connections:
            self.active_connections[machine_id].remove(websocket)
            logger.info(f"WebSocket disconnected for machine {machine_id}")

    async def broadcast_metrics(self, machine_id: str, message: dict):
        if machine_id in self.active_connections:
            for connection in self.active_connections[machine_id]:
                try:
                    await connection.send_json(message)
                except:
                    await self.disconnect(connection, machine_id)

manager = ConnectionManager()

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(STATIC['directory'], "index.html"))

@app.websocket("/ws/{machine_id}")
async def websocket_endpoint(websocket: WebSocket, machine_id: str):
    machine = get_vention_machine(machine_id)
    if not machine:
        await websocket.close(code=4004, reason=f"Machine {machine_id} not found")
        return

    await manager.connect(websocket, machine_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "get_metrics":
                metrics = {
                    "motion_state": machine.simulator.motion_state,
                    "safety_status": machine.simulator.safety_status,
                    "eco_metrics": machine.simulator.eco_metrics,
                    "system_status": machine.simulator.system_status,
                    "maintenance_state": machine.simulator.maintenance_state,
                    "vehicle_metrics": {
                        "production": {
                            "daily_output": 85,
                            "quality_score": 97.5,
                            "cycle_time": 42
                        },
                        "battery": {
                            "capacity": VEHICLE['requirements']['battery_capacity'],
                            "charge_rate": VEHICLE['requirements']['charging_rate'],
                            "temperature": 35
                        },
                        "safety": {
                            "crash_rating": "5 Stars",
                            "features_status": "All Systems Operational",
                            "compliance_score": 98
                        }
                    }
                }
                await websocket.send_json(metrics)
    except WebSocketDisconnect:
        manager.disconnect(websocket, machine_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, machine_id)

# API endpoints
@app.post("/models/", response_model=Model)
def create_model(model: ModelBase):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    now = datetime.utcnow()
    
    c.execute('''
        INSERT INTO models (name, type, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model.name, model.type, model.description, model.status, now, now))
    
    model_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": model_id,
        **model.dict(),
        "created_at": now,
        "updated_at": now
    }

@app.get("/models/", response_model=List[Model])
def get_models():
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('SELECT * FROM models')
    models = []
    for row in c.fetchall():
        models.append({
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "description": row[3],
            "status": row[4],
            "created_at": datetime.fromisoformat(row[5]),
            "updated_at": datetime.fromisoformat(row[6])
        })
    
    conn.close()
    return models

@app.post("/requirements/", response_model=Requirement)
def create_requirement(requirement: RequirementBase):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    now = datetime.utcnow()
    
    c.execute('''
        INSERT INTO requirements (title, description, status, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (requirement.title, requirement.description, requirement.status, 
          requirement.priority, now, now))
    
    req_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": req_id,
        **requirement.dict(),
        "created_at": now,
        "updated_at": now
    }

@app.get("/requirements/", response_model=List[Requirement])
def get_requirements():
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('SELECT * FROM requirements')
    requirements = []
    for row in c.fetchall():
        requirements.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "created_at": datetime.fromisoformat(row[5]),
            "updated_at": datetime.fromisoformat(row[6])
        })
    
    conn.close()
    return requirements

@app.post("/uml/", response_model=UMLDiagram)
def create_uml_diagram(diagram: UMLDiagramBase):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    now = datetime.utcnow()
    
    c.execute('''
        INSERT INTO uml_diagrams (title, type, content, model_id, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (diagram.title, diagram.type, diagram.content, diagram.model_id, now))
    
    diagram_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": diagram_id,
        **diagram.dict(),
        "created_at": now
    }

@app.get("/uml/", response_model=List[UMLDiagram])
def get_uml_diagrams():
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('SELECT * FROM uml_diagrams')
    diagrams = []
    for row in c.fetchall():
        diagrams.append({
            "id": row[0],
            "title": row[1],
            "type": row[2],
            "content": row[3],
            "model_id": row[4],
            "created_at": datetime.fromisoformat(row[5])
        })
    
    conn.close()
    return diagrams

@app.post("/metadata/", response_model=Metadata)
def create_metadata(metadata: MetadataBase):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    now = datetime.utcnow()
    
    c.execute('''
        INSERT INTO metadata (key, value, type, item_id, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (metadata.key, metadata.value, metadata.type, metadata.item_id, now))
    
    metadata_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": metadata_id,
        **metadata.dict(),
        "created_at": now
    }

@app.get("/metadata/", response_model=List[Metadata])
def get_metadata():
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('SELECT * FROM metadata')
    metadata_list = []
    for row in c.fetchall():
        metadata_list.append({
            "id": row[0],
            "key": row[1],
            "value": row[2],
            "type": row[3],
            "item_id": row[4],
            "created_at": datetime.fromisoformat(row[5])
        })
    
    conn.close()
    return metadata_list

@app.delete("/models/{model_id}")
def delete_model(model_id: int):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('DELETE FROM models WHERE id = ?', (model_id,))
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Model not found")
    
    conn.commit()
    conn.close()
    return {"message": "Model deleted successfully"}

@app.delete("/requirements/{req_id}")
def delete_requirement(req_id: int):
    conn = sqlite3.connect(DATABASE['requirements'])
    c = conn.cursor()
    
    c.execute('DELETE FROM requirements WHERE id = ?', (req_id,))
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    conn.commit()
    conn.close()
    return {"message": "Requirement deleted successfully"}

@app.get("/api/vention/machines")
def list_vention_machines():
    """List all available Vention machines"""
    return vention_api.list_machines()

@app.get("/api/vention/machines/{machine_id}")
def get_vention_machine(machine_id: str):
    """Get details of a specific Vention machine"""
    machine = vention_api.get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@app.get("/api/vention/machines/{machine_id}/components")
def get_machine_components(machine_id: str):
    """Get components of a specific Vention machine"""
    components = vention_api.get_machine_components(machine_id)
    if not components:
        raise HTTPException(status_code=404, detail="Machine or components not found")
    return components

@app.get("/api/vention/machines/{machine_id}/eco-metrics")
def get_machine_eco_metrics(machine_id: str):
    """Get environmental metrics for a specific Vention machine"""
    metrics = vention_api.get_eco_metrics(machine_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Machine or metrics not found")
    return metrics

@app.get("/api/vention/machines/{machine_id}/simulation")
def get_machine_simulation(machine_id: str):
    """Get simulation metrics for a specific machine"""
    machine = vention_api.get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine.get_simulation_metrics()

@app.post("/api/vention/machines/{machine_id}/move")
def move_machine_component(machine_id: str, move_request: MoveRequest):
    """Move a machine component to a specified position"""
    machine = vention_api.get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    success, message = machine.move_component(
        move_request.component_id,
        move_request.axis,
        move_request.position
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "success",
        "message": message,
        "metrics": machine.get_simulation_metrics()
    }

@app.post("/api/vention/machines/{machine_id}/move-coordinated")
def move_machine_coordinated(machine_id: str, move_request: CoordinatedMoveRequest):
    """Perform coordinated multi-axis motion"""
    machine = get_vention_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")
        
    try:
        result = machine.simulator.move_coordinated(move_request.positions)
        return {
            "status": "success",
            "message": "Coordinated move completed successfully",
            "metrics": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vention/machines/{machine_id}/sync-requirements")
def sync_machine_requirements_endpoint(machine_id: str):
    """Sync Vention machine specifications with requirements management system"""
    machine = vention_api.get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    requirements = sync_machine_requirements(machine)
    return requirements

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8004)
