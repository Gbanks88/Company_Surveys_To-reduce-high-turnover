from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from vention_simulation import VentionMachineSimulator
import random

class VentionMachineComponent(BaseModel):
    component_id: str
    name: str
    type: str
    dimensions: Dict[str, float]
    specifications: Dict[str, str]
    eco_metrics: Optional[Dict[str, float]] = None
    safety_status: Optional[Dict[str, bool]] = None
    motion_state: Optional[Dict[str, float]] = None
    position: Dict[str, float] = {"x": 0.0, "y": 0.0, "z": 0.0}

class VentionMachine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    machine_id: str
    name: str
    description: str = ""
    created_at: datetime
    components: List[VentionMachineComponent] = []
    total_weight: float = 0.0
    footprint: Dict[str, float] = {"length": 0.0, "width": 0.0, "height": 0.0}
    eco_score: float = 0.0
    simulator: Optional[VentionMachineSimulator] = None
    
    def model_post_init(self, __context):
        if self.simulator is None:
            self.simulator = VentionMachineSimulator()
        if not self.components:
            self.components = self._init_components()
    
    def _init_components(self) -> List[VentionMachineComponent]:
        """Initialize mock components"""
        return [
            VentionMachineComponent(
                component_id=f"comp_{i:03d}",
                name=f"Component {i}",
                type=random.choice(["linear_actuator", "rotary_actuator", "gripper"]),
                dimensions={"length": 200, "width": 150, "height": 100},
                specifications={
                    "power": "750W",
                    "efficiency": "95%",
                    "material": "recycled_aluminum"
                },
                eco_metrics={
                    "recycled_content": 85.0,
                    "energy_efficiency": 95.0,
                    "carbon_footprint": 120.5
                },
                position={"x": 0.0, "y": 0.0, "z": 0.0}
            )
            for i in range(1, 4)
        ]
    
    def get_components(self) -> List[VentionMachineComponent]:
        """Get list of machine components"""
        return self.components
    
    def get_component(self, component_id: str) -> Optional[VentionMachineComponent]:
        """Get specific component by ID"""
        return next((c for c in self.components if c.component_id == component_id), None)
    
    def move_component(self, component_id: str, axis: str, position: float) -> dict:
        """Move a component along specified axis"""
        component = self.get_component(component_id)
        if not component:
            raise ValueError(f"Component {component_id} not found")
        
        result = self.simulator.move_component(axis, position)
        component.position[axis] = position
        return result
    
    def get_simulation_metrics(self) -> dict:
        """Get current simulation metrics"""
        return {
            "motion_state": self.simulator.motion_state,
            "safety_status": self.simulator.safety_status,
            "eco_metrics": self.simulator.eco_metrics,
            "system_status": self.simulator.system_status,
            "maintenance_state": self.simulator.maintenance_state
        }

class MockVentionAPI:
    def __init__(self):
        self.machines: Dict[str, VentionMachine] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        # Mock eco-friendly machine example
        components = [
            VentionMachineComponent(
                component_id="comp_001",
                name="Eco Motor Assembly",
                type="motor",
                dimensions={"length": 200, "width": 150, "height": 100},
                specifications={
                    "power": "750W",
                    "efficiency": "95%",
                    "material": "recycled_aluminum"
                },
                eco_metrics={
                    "recycled_content": 85.0,
                    "energy_efficiency": 95.0,
                    "carbon_footprint": 120.5
                },
                position={"x": 0.0, "y": 0.0, "z": 0.0}
            ),
            VentionMachineComponent(
                component_id="comp_002",
                name="Solar Power Unit",
                type="power_supply",
                dimensions={"length": 300, "width": 200, "height": 50},
                specifications={
                    "output": "1000W",
                    "type": "solar_hybrid",
                    "material": "eco_composite"
                },
                eco_metrics={
                    "renewable_energy_ratio": 90.0,
                    "energy_efficiency": 92.0,
                    "carbon_footprint": 80.2
                },
                position={"x": 0.0, "y": 0.0, "z": 0.0}
            )
        ]

        self.machines["machine_001"] = VentionMachine(
            machine_id="machine_001",
            name="Eco-Automated Assembly Line",
            description="Energy-efficient automated assembly system",
            created_at=datetime.now(),
            components=components,
            total_weight=450.5,
            footprint={"length": 1200, "width": 800, "height": 1800},
            eco_score=92.5
        )

    def get_machine(self, machine_id: str) -> Optional[VentionMachine]:
        return self.machines.get(machine_id)

    def list_machines(self) -> List[VentionMachine]:
        return list(self.machines.values())

    def get_machine_components(self, machine_id: str) -> List[VentionMachineComponent]:
        machine = self.machines.get(machine_id)
        return machine.components if machine else []

    def get_eco_metrics(self, machine_id: str) -> Dict[str, float]:
        machine = self.machines.get(machine_id)
        if not machine:
            return {}
        
        total_carbon = sum(c.eco_metrics.get("carbon_footprint", 0) for c in machine.components)
        avg_efficiency = sum(c.eco_metrics.get("energy_efficiency", 0) for c in machine.components) / len(machine.components)
        
        return {
            "total_carbon_footprint": total_carbon,
            "average_energy_efficiency": avg_efficiency,
            "eco_score": machine.eco_score
        }

# Integration helper functions
def sync_machine_requirements(machine: VentionMachine) -> Dict[str, any]:
    """
    Synchronize Vention machine specifications with our requirements management system.
    This would normally interact with the actual Vention API.
    """
    requirements = {
        "mechanical": {
            "dimensions": machine.footprint,
            "weight": machine.total_weight,
            "components": len(machine.components)
        },
        "environmental": {
            "eco_score": machine.eco_score,
            "components": [
                {
                    "id": comp.component_id,
                    "eco_metrics": comp.eco_metrics
                }
                for comp in machine.components
            ]
        },
        "specifications": {
            comp.component_id: comp.specifications
            for comp in machine.components
        }
    }
    return requirements
