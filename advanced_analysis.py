import json
from collections import defaultdict
from typing import Dict, List, Set, Tuple

def load_data() -> List[Dict]:
    with open('company_structure.json', 'r') as f:
        return json.load(f)

class OrganizationAnalyzer:
    def __init__(self, employees_data: List[Dict]):
        self.employees = employees_data
        self.skill_groups = {
            'Technical': {
                'Software Engineer', 'DevOps Engineer', 'Systems Administrator',
                'Data Analyst', 'UX Designer', 'Quality Assurance'
            },
            'Business': {
                'Business Analyst', 'Sales Representative', 'Marketing Specialist',
                'Product Manager', 'Account Manager'
            },
            'Operations': {
                'Operations Specialist', 'HR Coordinator', 'Executive Assistant',
                'Customer Support'
            },
            'Professional': {
                'Legal Counsel', 'Financial Analyst', 'Research Analyst',
                'Content Writer'
            }
        }

    def analyze_skill_distribution(self) -> Dict:
        distribution = defaultdict(lambda: defaultdict(int))
        
        for emp in self.employees:
            if 'Manager' not in emp['position']:
                for group, roles in self.skill_groups.items():
                    if emp['position'] in roles:
                        distribution[group]['total'] += 1
                        distribution[group][emp['position']] += 1
        
        return distribution

    def analyze_team_diversity(self) -> List[Dict]:
        team_stats = []
        
        # Get all Level 1 managers
        managers = [emp for emp in self.employees if 'Level 1' in emp['position']]
        
        for manager in managers:
            team = [emp for emp in self.employees if emp.get('manager_id') == manager['id']]
            
            # Count roles in each skill group
            skill_counts = defaultdict(int)
            roles = set()
            
            for member in team:
                if 'Manager' not in member['position']:
                    roles.add(member['position'])
                    for group, group_roles in self.skill_groups.items():
                        if member['position'] in group_roles:
                            skill_counts[group] += 1
            
            team_stats.append({
                'manager_id': manager['id'],
                'team_size': len(team),
                'unique_roles': len(roles),
                'skill_distribution': dict(skill_counts)
            })
        
        return team_stats

    def find_collaboration_opportunities(self) -> List[Dict]:
        # Find teams that could benefit from cross-team collaboration
        teams = defaultdict(list)
        for emp in self.employees:
            if emp['manager_id']:
                teams[emp['manager_id']].append(emp)

        opportunities = []
        for manager_id, team in teams.items():
            skill_gaps = self.analyze_team_skill_gaps(team)
            if skill_gaps:
                opportunities.append({
                    'team_id': manager_id,
                    'team_size': len(team),
                    'skill_gaps': skill_gaps
                })
        
        return opportunities

    def analyze_team_skill_gaps(self, team: List[Dict]) -> List[str]:
        team_roles = {emp['position'] for emp in team}
        gaps = []
        
        # Check for missing key roles in each skill group
        for group, roles in self.skill_groups.items():
            roles_in_group = team_roles.intersection(roles)
            if len(roles_in_group) < 2:  # If team has less than 2 roles from a skill group
                missing_roles = roles - team_roles
                if missing_roles:
                    gaps.append(f"Need more {group} roles (missing: {', '.join(list(missing_roles)[:2])})")
        
        return gaps

def print_advanced_analysis():
    print("\n=== ADVANCED ORGANIZATIONAL ANALYSIS ===\n")
    
    analyzer = OrganizationAnalyzer(load_data())
    
    # 1. Skill Distribution Analysis
    print("1. SKILL DISTRIBUTION ACROSS ORGANIZATION")
    print("=" * 50)
    distribution = analyzer.analyze_skill_distribution()
    
    total_employees = sum(stats['total'] for stats in distribution.values())
    
    for group, stats in distribution.items():
        print(f"\n{group} Group:")
        print(f"Total: {stats['total']} employees ({stats['total']/total_employees*100:.1f}%)")
        print("Roles:")
        for role, count in stats.items():
            if role != 'total':
                print(f"  - {role}: {count} employees ({count/total_employees*100:.1f}%)")
    
    # 2. Team Diversity Analysis
    print("\n2. TEAM DIVERSITY ANALYSIS")
    print("=" * 50)
    team_stats = analyzer.analyze_team_diversity()
    
    # Find most and least diverse teams
    most_diverse = max(team_stats, key=lambda x: x['unique_roles'])
    least_diverse = min(team_stats, key=lambda x: x['unique_roles'])
    
    print("\nMost diverse team:")
    print(f"Manager ID: {most_diverse['manager_id']}")
    print(f"Team size: {most_diverse['team_size']}")
    print(f"Unique roles: {most_diverse['unique_roles']}")
    print("Skill distribution:")
    for group, count in most_diverse['skill_distribution'].items():
        print(f"  - {group}: {count} employees")
    
    print("\nLeast diverse team:")
    print(f"Manager ID: {least_diverse['manager_id']}")
    print(f"Team size: {least_diverse['team_size']}")
    print(f"Unique roles: {least_diverse['unique_roles']}")
    print("Skill distribution:")
    for group, count in least_diverse['skill_distribution'].items():
        print(f"  - {group}: {count} employees")

    # 3. Collaboration Opportunities
    print("\n\n3. COLLABORATION OPPORTUNITIES")
    print("=" * 50)
    opportunities = analyzer.find_collaboration_opportunities()
    
    print("\nTeams that could benefit from cross-team collaboration:")
    for opp in opportunities[:5]:  # Show top 5 opportunities
        print(f"\nTeam {opp['team_id']} (Size: {opp['team_size']})")
        for gap in opp['skill_gaps']:
            print(f"  - {gap}")

if __name__ == "__main__":
    print_advanced_analysis()
