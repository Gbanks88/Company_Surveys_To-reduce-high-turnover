from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import math
import numpy as np

@dataclass
class MotionState:
    position: Dict[str, float]
    velocity: Dict[str, float]
    acceleration: Dict[str, float]
    is_moving: bool
    is_homed: bool
    safety_status: Dict[str, bool]

class MotionProfile:
    def __init__(self, max_velocity: float, max_acceleration: float, max_jerk: float):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.max_jerk = max_jerk
        
    def calculate_s_curve(self, distance: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Generate S-curve motion profile with jerk limiting"""
        # Time periods for each phase
        t_j = self.max_acceleration / self.max_jerk  # Time to reach max acceleration
        t_a = self.max_velocity / self.max_acceleration  # Time to reach max velocity
        
        # Calculate minimum distance for full S-curve
        d_min = self.max_velocity * t_a
        
        if distance < d_min:
            # Short move - triangular velocity profile
            t_a = math.sqrt(distance / self.max_acceleration)
            t_j = t_a / 2
            max_v = self.max_acceleration * t_a
        else:
            max_v = self.max_velocity
            
        # Generate time points
        dt = 0.001  # 1ms intervals
        t_total = t_a * 2 + t_j * 4
        t = np.arange(0, t_total, dt)
        
        # Initialize arrays
        pos = np.zeros_like(t)
        vel = np.zeros_like(t)
        acc = np.zeros_like(t)
        
        # Generate profile segments
        for i, time in enumerate(t):
            if time <= t_j:  # Initial jerk
                acc[i] = self.max_jerk * time
                vel[i] = self.max_jerk * time**2 / 2
                pos[i] = self.max_jerk * time**3 / 6
            elif time <= t_a:  # Constant acceleration
                acc[i] = self.max_acceleration
                vel[i] = self.max_acceleration * time
                pos[i] = self.max_acceleration * time**2 / 2
            elif time <= t_a + t_j:  # Deceleration jerk
                t_rel = time - t_a
                acc[i] = self.max_acceleration - self.max_jerk * t_rel
                vel[i] = max_v - self.max_acceleration * t_rel**2 / 2
                pos[i] = max_v * time - self.max_acceleration * t_rel**3 / 6
            else:  # Constant velocity
                acc[i] = 0
                vel[i] = max_v
                pos[i] = max_v * time
                
        return pos, vel, acc, t_total

class MaintenancePredictor:
    def __init__(self):
        self.cycle_count = 0
        self.total_distance = 0
        self.total_time = 0
        self.peak_temperatures = []
        self.vibration_history = []
        self.fault_history = []
        
    def update_metrics(self, distance: float, time: float, temperature: float, vibration: float):
        self.cycle_count += 1
        self.total_distance += distance
        self.total_time += time
        self.peak_temperatures.append(temperature)
        self.vibration_history.append(vibration)
        
    def calculate_health_metrics(self) -> Dict:
        # Component wear calculation
        wear_factor = self.total_distance / 1000000  # Assume 1M mm is baseline
        
        # Temperature stress
        temp_stress = 0
        if len(self.peak_temperatures) > 0:
            avg_temp = sum(self.peak_temperatures) / len(self.peak_temperatures)
            temp_stress = max(0, (avg_temp - 25) / 50)  # Normalize to 0-1
            
        # Vibration analysis
        vibration_trend = 0
        if len(self.vibration_history) > 10:
            recent_vib = np.mean(self.vibration_history[-10:])
            vibration_trend = recent_vib / 0.8  # Normalize to baseline
            
        # Calculate remaining life
        base_life = 10000  # Base cycles
        adjusted_life = base_life * (1 - wear_factor) * (1 - temp_stress) * (1 - vibration_trend)
        remaining_cycles = max(0, adjusted_life - self.cycle_count)
        
        # Maintenance urgency score
        urgency_score = min(1.0, (
            0.4 * wear_factor +
            0.3 * temp_stress +
            0.3 * vibration_trend
        ))
        
        return {
            "remaining_cycles": remaining_cycles,
            "wear_factor": wear_factor,
            "temperature_stress": temp_stress,
            "vibration_trend": vibration_trend,
            "maintenance_urgency": urgency_score,
            "estimated_remaining_hours": remaining_cycles * 0.1  # Assume 0.1 hours per cycle
        }

class VentionMachineSimulator:
    def __init__(self):
        self.reset_state()
        self.motion_profile = MotionProfile(
            max_velocity=500.0,    # mm/s
            max_acceleration=1000.0,  # mm/s²
            max_jerk=5000.0       # mm/s³
        )
        self.maintenance_predictor = MaintenancePredictor()
        
    def reset_state(self):
        """Initialize or reset simulator state"""
        self.motion_state = {
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
            "acceleration": {"x": 0.0, "y": 0.0, "z": 0.0},
            "is_moving": False,
            "is_homed": False
        }
        
        self.safety_status = {
            "e_stop": False,
            "safety_door": True,
            "limit_switch": False,
            "motor_fault": False,
            "collision_risk": 0.0,
            "vibration_level": 0.0,
            "temperature": 25.0,
            "maintenance_due": False,
            "safety_zone_violations": 0,
            "operator_proximity": "safe"
        }
        
        self.eco_metrics = {
            "power_consumption": 0.0,
            "total_energy": 0.0,
            "efficiency": 85.0,
            "carbon_footprint": 0.0,
            "optimization_score": 92.5,
            "peak_power": 0.0,
            "energy_recovery": 0.0,
            "standby_power": 15.0,
            "power_factor": 0.95,
            "thermal_efficiency": 92.0,
            "renewable_energy_ratio": 0.3,
            "waste_heat": 0.0,
            "lifecycle_emissions": 0.0
        }
        
        self.system_status = {
            "power": 0.0,
            "current": 0.0,
            "voltage": 24.0,
            "uptime": 0,
            "cycles_completed": 0,
            "mean_time_between_failures": 8760,
            "predicted_maintenance": 2000
        }
        
        self.coordinated_motion = {
            "in_progress": False,
            "path_complete": 0.0,
            "path_length": 0.0,
            "interpolation_time": 0.0,
            "synchronized_axes": []
        }
        
        self.maintenance_state = {
            "component_health": 1.0,
            "predicted_failures": [],
            "maintenance_schedule": [],
            "wear_metrics": {},
            "health_trends": []
        }

    def calculate_motion_metrics(self, distance):
        """Calculate motion-related metrics based on movement distance"""
        # Basic motion calculations
        acceleration = 1000.0  # mm/s^2
        max_velocity = 500.0   # mm/s
        
        # Time calculations
        accel_time = max_velocity / acceleration
        accel_distance = 0.5 * acceleration * accel_time ** 2
        
        if distance <= 2 * accel_distance:
            # Triangle profile
            total_time = 2 * math.sqrt(distance / acceleration)
            peak_velocity = math.sqrt(acceleration * distance)
        else:
            # Trapezoid profile
            constant_velocity_distance = distance - 2 * accel_distance
            constant_velocity_time = constant_velocity_distance / max_velocity
            total_time = 2 * accel_time + constant_velocity_time
            peak_velocity = max_velocity
            
        # Update motion state
        self.motion_state["is_moving"] = True
        self.motion_state["velocity"]["x"] = peak_velocity
        self.motion_state["acceleration"]["x"] = acceleration
        
        return total_time, peak_velocity

    def calculate_power_consumption(self, distance, time):
        """Calculate power consumption and related metrics"""
        # Base calculations
        mass = 5.0  # kg
        gravity = 9.81  # m/s^2
        friction_coefficient = 0.1
        
        # Work calculations
        friction_force = mass * gravity * friction_coefficient
        work_against_friction = friction_force * (distance / 1000)  # Convert mm to m
        
        # Power calculations
        average_power = work_against_friction / time
        peak_power = average_power * 2.5  # Assume peak is 2.5x average
        
        # Energy calculations
        total_energy = average_power * time
        recoverable_energy = total_energy * 0.15  # 15% energy recovery
        
        # Update eco metrics
        self.eco_metrics["power_consumption"] = average_power
        self.eco_metrics["peak_power"] = peak_power
        self.eco_metrics["total_energy"] = total_energy
        self.eco_metrics["energy_recovery"] = recoverable_energy
        self.eco_metrics["waste_heat"] = total_energy * 0.08  # 8% heat loss
        
        # Calculate emissions
        grid_emission_factor = 0.5  # kg CO2/kWh
        self.eco_metrics["carbon_footprint"] = (total_energy / 3600000) * grid_emission_factor  # Convert J to kWh
        self.eco_metrics["lifecycle_emissions"] = self.eco_metrics["carbon_footprint"] * 1.2  # Include manufacturing emissions
        
        # Update system status
        self.system_status["power"] = average_power
        self.system_status["current"] = average_power / self.system_status["voltage"]
        
        return average_power

    def update_safety_metrics(self, distance, velocity):
        """Update safety-related metrics based on motion"""
        # Collision risk calculation
        self.safety_status["collision_risk"] = min((velocity / 1000.0) * 0.1, 1.0)  # 0-1 scale
        
        # Vibration calculation based on velocity and acceleration
        self.safety_status["vibration_level"] = (velocity / 500.0) * 0.8  # 0-1 scale
        
        # Temperature increase simulation
        base_temp = 25.0
        temp_increase = (velocity / 500.0) * 5.0  # Up to 5 degrees increase
        self.safety_status["temperature"] = base_temp + temp_increase
        
        # Maintenance prediction
        self.system_status["cycles_completed"] += 1
        if self.system_status["cycles_completed"] > self.system_status["predicted_maintenance"]:
            self.safety_status["maintenance_due"] = True
            
        # Safety zone monitoring
        if distance > 800:  # Example safety zone limit
            self.safety_status["safety_zone_violations"] += 1
            
        # Update operator proximity based on motion
        if velocity > 400:
            self.safety_status["operator_proximity"] = "restricted"
        elif velocity > 200:
            self.safety_status["operator_proximity"] = "caution"
        else:
            self.safety_status["operator_proximity"] = "safe"

    def calculate_coordinated_motion(self, target_positions: Dict[str, float]) -> Tuple[Dict, float]:
        """Calculate coordinated multi-axis motion profile"""
        # Calculate total path length
        current_pos = self.motion_state["position"]
        path_vector = {axis: target_positions[axis] - current_pos[axis] 
                      for axis in target_positions.keys()}
        
        path_length = math.sqrt(sum(d*d for d in path_vector.values()))
        
        # Generate master motion profile
        pos_profile, vel_profile, acc_profile, total_time = self.motion_profile.calculate_s_curve(path_length)
        
        # Calculate scale factors for each axis
        scale_factors = {axis: path_vector[axis]/path_length 
                        for axis in path_vector.keys()}
        
        # Generate individual axis profiles
        axis_profiles = {}
        for axis, scale in scale_factors.items():
            axis_profiles[axis] = {
                "position": pos_profile * scale,
                "velocity": vel_profile * scale,
                "acceleration": acc_profile * scale
            }
            
        return axis_profiles, total_time

    def update_maintenance_predictions(self, motion_data: Dict):
        """Update maintenance predictions based on motion data"""
        # Extract relevant metrics
        distance = motion_data.get("distance", 0)
        time = motion_data.get("time", 0)
        temperature = self.safety_status["temperature"]
        vibration = self.safety_status["vibration_level"]
        
        # Update maintenance predictor
        self.maintenance_predictor.update_metrics(
            distance=distance,
            time=time,
            temperature=temperature,
            vibration=vibration
        )
        
        # Get updated health metrics
        health_metrics = self.maintenance_predictor.calculate_health_metrics()
        
        # Update maintenance state
        self.maintenance_state["component_health"] = max(0.0, 1.0 - health_metrics["maintenance_urgency"])
        self.maintenance_state["wear_metrics"] = health_metrics
        
        # Generate maintenance schedule
        if health_metrics["maintenance_urgency"] > 0.7:
            self.maintenance_state["predicted_failures"].append({
                "component": "motion_system",
                "predicted_time": health_metrics["estimated_remaining_hours"],
                "confidence": health_metrics["maintenance_urgency"],
                "recommended_action": "Immediate maintenance required"
            })
        elif health_metrics["maintenance_urgency"] > 0.4:
            self.maintenance_state["maintenance_schedule"].append({
                "component": "motion_system",
                "due_in_hours": health_metrics["estimated_remaining_hours"],
                "type": "Preventive",
                "priority": "Medium"
            })

    def move_component(self, axis: str, position: float) -> dict:
        """Enhanced component movement with sophisticated motion profiles"""
        current_pos = self.motion_state["position"][axis]
        distance = abs(position - current_pos)
        
        # Generate motion profile
        pos_profile, vel_profile, acc_profile, total_time = self.motion_profile.calculate_s_curve(distance)
        
        # Calculate power and energy metrics
        average_power = self.calculate_power_consumption(distance, total_time)
        
        # Update safety metrics
        peak_velocity = np.max(vel_profile)
        self.update_safety_metrics(distance, peak_velocity)
        
        # Update maintenance predictions
        self.update_maintenance_predictions({
            "distance": distance,
            "time": total_time,
            "peak_velocity": peak_velocity,
            "peak_acceleration": np.max(acc_profile)
        })
        
        # Update final position
        self.motion_state["position"][axis] = position
        
        # Calculate optimization score with maintenance factor
        efficiency_score = 100 * (1 - (average_power / 2000))
        safety_score = 100 * (1 - self.safety_status["collision_risk"])
        thermal_score = 100 * (1 - ((self.safety_status["temperature"] - 25) / 10))
        maintenance_score = 100 * self.maintenance_state["component_health"]
        
        self.eco_metrics["optimization_score"] = (
            efficiency_score * 0.3 +
            safety_score * 0.3 +
            thermal_score * 0.2 +
            maintenance_score * 0.2
        )
        
        # Reset motion state
        self.motion_state["is_moving"] = False
        self.motion_state["velocity"][axis] = 0.0
        self.motion_state["acceleration"][axis] = 0.0
        
        return {
            "motion_state": self.motion_state,
            "safety_status": self.safety_status,
            "eco_metrics": self.eco_metrics,
            "system_status": self.system_status,
            "maintenance_state": self.maintenance_state
        }

    def move_coordinated(self, target_positions: Dict[str, float]) -> dict:
        """Perform coordinated multi-axis motion"""
        # Validate target positions
        for axis, pos in target_positions.items():
            if axis not in self.motion_state["position"]:
                raise ValueError(f"Invalid axis: {axis}")
        
        # Calculate coordinated motion profiles
        axis_profiles, total_time = self.calculate_coordinated_motion(target_positions)
        
        # Calculate total path length
        path_length = math.sqrt(sum(
            (target_positions[axis] - self.motion_state["position"][axis])**2
            for axis in target_positions.keys()
        ))
        
        # Update coordinated motion state
        self.coordinated_motion["in_progress"] = True
        self.coordinated_motion["path_length"] = path_length
        self.coordinated_motion["synchronized_axes"] = list(target_positions.keys())
        
        # Simulate motion execution
        for axis, target in target_positions.items():
            self.motion_state["position"][axis] = target
        
        # Calculate power and update metrics
        average_power = self.calculate_power_consumption(path_length, total_time)
        peak_velocity = max(max(p["velocity"]) for p in axis_profiles.values())
        self.update_safety_metrics(path_length, peak_velocity)
        
        # Update maintenance predictions
        self.update_maintenance_predictions({
            "distance": path_length,
            "time": total_time,
            "peak_velocity": peak_velocity,
            "peak_acceleration": max(max(p["acceleration"]) for p in axis_profiles.values())
        })
        
        # Reset coordinated motion state
        self.coordinated_motion["in_progress"] = False
        self.coordinated_motion["path_complete"] = 100.0
        
        return {
            "motion_state": self.motion_state,
            "safety_status": self.safety_status,
            "eco_metrics": self.eco_metrics,
            "system_status": self.system_status,
            "maintenance_state": self.maintenance_state,
            "coordinated_motion": self.coordinated_motion
        }

    def move_to_position(self, axis: str, target: float) -> Tuple[bool, str]:
        """Simulate moving to an absolute position"""
        if not self._check_safety():
            return False, "Safety check failed"
        
        if not self._validate_position(axis, target):
            return False, f"Position {target} is outside workspace limits for axis {axis}"
        
        current_pos = self.current_state.position[axis]
        distance = target - current_pos
        
        # Calculate motion profile
        max_v = self.motion_limits["max_velocity"]
        max_a = self.motion_limits["max_acceleration"]
        
        # Simple trapezoidal motion profile
        t_acc = max_v / max_a
        d_acc = 0.5 * max_a * t_acc * t_acc
        
        if abs(distance) < 2 * d_acc:
            # Triangular profile for short moves
            peak_v = math.sqrt(abs(distance) * max_a)
            t_total = 2 * peak_v / max_a
        else:
            # Trapezoidal profile
            t_const = (abs(distance) - 2 * d_acc) / max_v
            t_total = 2 * t_acc + t_const
        
        # Update energy consumption
        power = self._calculate_power_consumption(distance, t_total)
        self.energy_consumption["power"] = power
        self.energy_consumption["total_energy"] += power * (t_total / 3600.0)  # Convert to Wh
        
        # Update position
        self.current_state.position[axis] = target
        return True, "Move completed successfully"

    def get_eco_metrics(self) -> Dict[str, float]:
        """Get environmental impact metrics"""
        return {
            "power_consumption": self.energy_consumption["power"],
            "total_energy": self.energy_consumption["total_energy"],
            "efficiency": self._calculate_efficiency(),
            "carbon_footprint": self._estimate_carbon_footprint(),
            "optimization_score": self._calculate_optimization_score()
        }

    def get_safety_status(self) -> Dict[str, bool]:
        """Get current safety status"""
        return self.current_state.safety_status

    def _check_safety(self) -> bool:
        """Check if all safety conditions are met"""
        return (not self.current_state.safety_status["e_stop"] and
                self.current_state.safety_status["safety_door"] and
                not self.current_state.safety_status["limit_switch"] and
                not self.current_state.safety_status["motor_fault"])

    def _validate_position(self, axis: str, position: float) -> bool:
        """Check if position is within workspace limits"""
        min_pos, max_pos = self.motion_limits["workspace_limits"][axis]
        return min_pos <= position <= max_pos

    def _calculate_power_consumption(self, distance: float, time: float) -> float:
        """Calculate power consumption for a move"""
        # Simple model: P = F * v = m * a * v
        mass = 5.0  # kg (example mass)
        avg_velocity = distance / time
        avg_acceleration = 2 * distance / (time * time)
        force = mass * avg_acceleration
        power = force * avg_velocity
        return abs(power)  # Convert to positive watts

    def _calculate_efficiency(self) -> float:
        """Calculate current system efficiency"""
        # Example efficiency calculation (0-100%)
        base_efficiency = 85.0  # Base efficiency percentage
        velocity_factor = 1.0 - (max(abs(v) for v in self.current_state.velocity.values()) / self.motion_limits["max_velocity"])
        return base_efficiency * velocity_factor

    def _estimate_carbon_footprint(self) -> float:
        """Estimate carbon footprint in kg CO2e"""
        # Example: 0.5 kg CO2e per kWh of electricity
        energy_kwh = self.energy_consumption["total_energy"] / 1000.0
        return energy_kwh * 0.5

    def _calculate_optimization_score(self) -> float:
        """Calculate overall optimization score (0-100)"""
        efficiency_score = self._calculate_efficiency()
        energy_score = 100.0 * (1.0 - min(self.energy_consumption["power"] / 1000.0, 1.0))
        return (efficiency_score + energy_score) / 2.0
