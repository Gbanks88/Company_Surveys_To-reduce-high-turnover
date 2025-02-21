import random
import math
from typing import List, Dict
import json

# Specialized support team positions
SOFTWARE_SUPPORT_ROLES = [
    "Software Engineer",
    "DevOps Engineer",
    "QA Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Database Administrator",
    "Cloud Engineer",
    "Systems Analyst",
    "Application Support Specialist",
    "Integration Specialist"
]

HARDWARE_SUPPORT_ROLES = [
    "Hardware Engineer",
    "Network Engineer",
    "Systems Administrator",
    "Infrastructure Specialist",
    "Data Center Technician",
    "Network Administrator",
    "Security Engineer",
    "IT Support Specialist",
    "Equipment Technician",
    "Hardware Analyst"
]

MAINTENANCE_SUPPORT_ROLES = [
    "Maintenance Engineer",
    "Facilities Manager",
    "Preventive Maintenance Specialist",
    "Repair Technician",
    "Equipment Maintenance Specialist",
    "Maintenance Coordinator",
    "Safety Inspector",
    "Inventory Manager",
    "Maintenance Planner",
    "Quality Control Specialist"
]

# General business and support positions
GENERAL_POSITIONS = [
    "Project Manager",
    "Business Analyst",
    "Technical Writer",
    "Customer Support Representative",
    "Operations Coordinator",
    "Administrative Assistant",
    "Training Specialist",
    "Documentation Specialist",
    "Resource Coordinator",
    "Team Lead"
]

class Employee:
    def __init__(self, id: int, position: str, team_type: str, level: int = 0):
        self.id = id
        self.position = position
        self.team_type = team_type
        self.level = level
        self.manager = None
        self.subordinates = []

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'position': self.position,
            'team_type': self.team_type,
            'level': self.level,
            'manager_id': self.manager.id if self.manager else None,
            'subordinates': [sub.id for sub in self.subordinates]
        }

def create_support_team(start_id: int, team_type: str, team_size: int) -> List[Employee]:
    employees = []
    role_list = {
        "Software": SOFTWARE_SUPPORT_ROLES,
        "Hardware": HARDWARE_SUPPORT_ROLES,
        "Maintenance": MAINTENANCE_SUPPORT_ROLES
    }[team_type]
    
    # Create team manager
    manager = Employee(
        id=start_id,
        position=f"{team_type} Support Manager",
        team_type=team_type,
        level=1
    )
    employees.append(manager)
    
    # Create specialized team members
    for i in range(team_size - 1):
        position = random.choice(role_list)
        employee = Employee(
            id=start_id + i + 1,
            position=position,
            team_type=team_type
        )
        employee.manager = manager
        manager.subordinates.append(employee)
        employees.append(employee)
    
    # Add some general support positions
    for i in range(3):  # Add 3 general support positions to each team
        position = random.choice(GENERAL_POSITIONS)
        employee = Employee(
            id=start_id + team_size + i,
            position=position,
            team_type=team_type
        )
        employee.manager = manager
        manager.subordinates.append(employee)
        employees.append(employee)
    
    return employees

def create_company_structure(total_employees: int = 500) -> List[Employee]:
    employees = []
    current_id = 1
    
    # Create Director of Support Services
    director = Employee(
        id=current_id,
        position="Director of Support Services",
        team_type="Management",
        level=2
    )
    employees.append(director)
    current_id += 1
    
    # Calculate team sizes (approximately equal distribution)
    base_team_size = (total_employees - 1) // 3  # -1 for director
    
    # Create Software Support Team
    software_team = create_support_team(current_id, "Software", base_team_size)
    software_team[0].manager = director  # Set manager for team lead
    director.subordinates.append(software_team[0])
    employees.extend(software_team)
    current_id += len(software_team)
    
    # Create Hardware Support Team
    hardware_team = create_support_team(current_id, "Hardware", base_team_size)
    hardware_team[0].manager = director
    director.subordinates.append(hardware_team[0])
    employees.extend(hardware_team)
    current_id += len(hardware_team)
    
    # Create Maintenance Support Team
    maintenance_team = create_support_team(current_id, "Maintenance", base_team_size)
    maintenance_team[0].manager = director
    director.subordinates.append(maintenance_team[0])
    employees.extend(maintenance_team)
    
    return employees

def generate_team_report(employees: List[Employee]) -> Dict:
    teams = {
        "Software": {"count": 0, "roles": {}},
        "Hardware": {"count": 0, "roles": {}},
        "Maintenance": {"count": 0, "roles": {}}
    }
    
    for emp in employees:
        if emp.team_type in teams:
            teams[emp.team_type]["count"] += 1
            if emp.position in teams[emp.team_type]["roles"]:
                teams[emp.team_type]["roles"][emp.position] += 1
            else:
                teams[emp.team_type]["roles"][emp.position] = 1
    
    return teams

def main():
    # Create company structure
    employees = create_company_structure(500)
    
    # Generate team report
    team_report = generate_team_report(employees)
    
    # Convert all employees to dictionary format
    employee_data = [emp.to_dict() for emp in employees]
    
    # Save data to JSON files
    with open('support_teams.json', 'w') as f:
        json.dump(team_report, f, indent=2)
    
    with open('support_structure.json', 'w') as f:
        json.dump(employee_data, f, indent=2)
    
    # Print summary
    print("\nSupport Teams Structure Generated!")
    print("=" * 50)
    
    for team_type, data in team_report.items():
        print(f"\n{team_type} Support Team:")
        print(f"Total members: {data['count']}")
        print("\nRole distribution:")
        for role, count in data['roles'].items():
            print(f"  - {role}: {count} members")

if __name__ == "__main__":
    main()
