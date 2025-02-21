import json
from collections import Counter
from typing import Dict, List

def analyze_company_structure():
    # Load the company structure data
    with open('company_structure.json', 'r') as f:
        employees = json.load(f)
    
    # Analyze position distribution
    positions = Counter(emp['position'] for emp in employees)
    
    # Analyze management structure
    management_levels = Counter(emp['level'] for emp in employees)
    
    # Analyze span of control
    span_of_control = Counter(len(emp['subordinates']) for emp in employees if emp['subordinates'])
    
    # Find the reporting chains
    def find_chain(emp_id):
        chain = []
        current = next(emp for emp in employees if emp['id'] == emp_id)
        while current['manager_id'] is not None:
            chain.append(current['position'])
            current = next(emp for emp in employees if emp['id'] == current['manager_id'])
        chain.append(current['position'])
        return chain
    
    # Get a sample reporting chain
    sample_emp = next(emp for emp in employees if emp['level'] == 0)
    sample_chain = find_chain(sample_emp['id'])
    
    # Print detailed analysis
    print("\n=== DETAILED COMPANY ANALYSIS ===\n")
    
    print("POSITION DISTRIBUTION:")
    for position, count in sorted(positions.items()):
        if "Manager" not in position and "CEO" not in position:
            print(f"{position}: {count} employees")
    
    print("\nMANAGEMENT STRUCTURE:")
    for level, count in sorted(management_levels.items()):
        print(f"Level {level}: {count} employees")
    
    print("\nMANAGERIAL SPAN OF CONTROL:")
    for span, count in sorted(span_of_control.items()):
        print(f"Managers with {span} direct reports: {count}")
    
    print("\nSAMPLE REPORTING CHAIN (bottom to top):")
    for i, position in enumerate(sample_chain):
        print(f"Level {i}: {position}")
    
    # Find the largest and smallest teams
    team_sizes = [(emp['id'], len(emp['subordinates'])) for emp in employees if emp['subordinates']]
    largest_team = max(team_sizes, key=lambda x: x[1])
    smallest_team = min(team_sizes, key=lambda x: x[1])
    
    print("\nTEAM SIZE ANALYSIS:")
    print(f"Largest team size: {largest_team[1]} (Manager ID: {largest_team[0]})")
    print(f"Smallest team size: {smallest_team[1]} (Manager ID: {smallest_team[0]})")

if __name__ == "__main__":
    analyze_company_structure()
