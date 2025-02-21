import json
from typing import Dict, List, Optional
from collections import defaultdict

class EmployeeNode:
    def __init__(self, id: int, position: str, level: int):
        self.id = id
        self.position = position
        self.level = level
        self.subordinates: List[EmployeeNode] = []
        self.manager: Optional[EmployeeNode] = None

def build_org_tree(employees_data: List[Dict]) -> Dict[int, EmployeeNode]:
    # Create nodes for all employees
    nodes = {}
    for emp in employees_data:
        nodes[emp['id']] = EmployeeNode(emp['id'], emp['position'], emp['level'])
    
    # Build relationships
    for emp in employees_data:
        if emp['manager_id']:
            nodes[emp['id']].manager = nodes[emp['manager_id']]
            nodes[emp['manager_id']].subordinates.append(nodes[emp['id']])
    
    return nodes

def print_team_composition(manager_node: EmployeeNode, indent: int = 0):
    prefix = "  " * indent
    print(f"{prefix}📊 {manager_node.position} (ID: {manager_node.id})")
    
    # Group subordinates by position
    positions = defaultdict(list)
    for sub in manager_node.subordinates:
        positions[sub.position].append(sub)
    
    # Print team composition
    for position, employees in positions.items():
        if "Manager" not in position:
            print(f"{prefix}  └─ {position}: {len(employees)} employee(s)")

def analyze_detailed_structure():
    # Load the company structure data
    with open('company_structure.json', 'r') as f:
        employees_data = json.load(f)
    
    # Build organization tree
    nodes = build_org_tree(employees_data)
    
    # Find top-level managers (Level 2)
    top_managers = [node for node in nodes.values() if node.level == 2]
    
    print("\n=== DETAILED ORGANIZATIONAL HIERARCHY ===\n")
    
    # Analyze each top-level manager's organization
    for top_manager in top_managers:
        print("\n" + "="*50)
        print(f"\nORGANIZATION UNDER {top_manager.position} (ID: {top_manager.id})")
        print("="*50)
        
        # Print direct reports (Level 1 managers)
        print(f"\nDirect Reports ({len(top_manager.subordinates)} Level 1 Managers):")
        for i, manager in enumerate(top_manager.subordinates, 1):
            print(f"\n🔹 TEAM {i}")
            print_team_composition(manager, indent=1)
    
    # Calculate some interesting statistics
    technical_roles = {'Software Engineer', 'DevOps Engineer', 'Systems Administrator', 'Data Analyst'}
    business_roles = {'Business Analyst', 'Product Manager', 'Sales Representative', 'Marketing Specialist'}
    
    role_counts = defaultdict(int)
    tech_count = 0
    business_count = 0
    
    for emp in employees_data:
        if 'Manager' not in emp['position']:
            role_counts[emp['position']] += 1
            if emp['position'] in technical_roles:
                tech_count += 1
            elif emp['position'] in business_roles:
                business_count += 1
    
    print("\n" + "="*50)
    print("\nWORKFORCE DISTRIBUTION ANALYSIS")
    print("="*50)
    
    print("\nTechnical vs Business Ratio:")
    print(f"Technical Roles: {tech_count} employees ({tech_count/5:.1f}%)")
    print(f"Business Roles: {business_count} employees ({business_count/5:.1f}%)")
    print(f"Other Roles: {500-tech_count-business_count} employees ({(500-tech_count-business_count)/5:.1f}%)")
    
    print("\nTop 5 Largest Departments:")
    top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for role, count in top_roles:
        print(f"- {role}: {count} employees ({count/5:.1f}%)")

if __name__ == "__main__":
    analyze_detailed_structure()
