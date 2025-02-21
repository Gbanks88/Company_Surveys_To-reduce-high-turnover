import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from scipy import stats
from typing import Dict, List, Tuple
import random

class EmployeeSurveySystem:
    def __init__(self):
        # Load employee structure
        with open('support_structure.json', 'r') as f:
            self.employees = json.load(f)
        
        self.questions = [
            "How was your day? (1-5)",
            "What did you accomplish today? (1-5)",
            "Are you happy with your work? (1-5)"
        ]
        
        # Initialize survey data structure
        self.survey_data = {
            'employee_id': [],
            'team_type': [],
            'date': [],
            'day_rating': [],
            'accomplishment_rating': [],
            'happiness_rating': []
        }

    def generate_yearly_survey_data(self):
        """Generate synthetic survey data for one year"""
        start_date = datetime(2024, 1, 1)
        
        # Generate weekly responses for each employee
        for employee in self.employees:
            # Skip the director
            if employee['position'] == "Director of Support Services":
                continue
            
            # Employee's base satisfaction levels (different for each employee)
            base_day_rating = np.random.normal(3.5, 0.5)
            base_accomplishment = np.random.normal(3.8, 0.4)
            base_happiness = np.random.normal(3.7, 0.3)
            
            # Generate 52 weeks of data
            for week in range(52):
                current_date = start_date + timedelta(weeks=week)
                
                # Add some random variation and seasonal effects
                seasonal_effect = np.sin(week * 2 * np.pi / 52) * 0.3
                
                # Generate ratings with some randomness and seasonal effects
                day_rating = max(1, min(5, base_day_rating + seasonal_effect + np.random.normal(0, 0.3)))
                accomplishment = max(1, min(5, base_accomplishment + seasonal_effect + np.random.normal(0, 0.2)))
                happiness = max(1, min(5, base_happiness + seasonal_effect + np.random.normal(0, 0.25)))
                
                # Store the data
                self.survey_data['employee_id'].append(employee['id'])
                self.survey_data['team_type'].append(employee['team_type'])
                self.survey_data['date'].append(current_date)
                self.survey_data['day_rating'].append(round(day_rating))
                self.survey_data['accomplishment_rating'].append(round(accomplishment))
                self.survey_data['happiness_rating'].append(round(happiness))

    def calculate_descriptive_statistics(self) -> Dict:
        """Calculate descriptive statistics for survey responses"""
        df = pd.DataFrame(self.survey_data)
        
        stats_by_team = {}
        for team in ['Software', 'Hardware', 'Maintenance']:
            team_data = df[df['team_type'] == team]
            
            stats_by_team[team] = {
                'day_rating': {
                    'mean': team_data['day_rating'].mean(),
                    'median': team_data['day_rating'].median(),
                    'mode': team_data['day_rating'].mode().iloc[0],
                    'std': team_data['day_rating'].std()
                },
                'accomplishment_rating': {
                    'mean': team_data['accomplishment_rating'].mean(),
                    'median': team_data['accomplishment_rating'].median(),
                    'mode': team_data['accomplishment_rating'].mode().iloc[0],
                    'std': team_data['accomplishment_rating'].std()
                },
                'happiness_rating': {
                    'mean': team_data['happiness_rating'].mean(),
                    'median': team_data['happiness_rating'].median(),
                    'mode': team_data['happiness_rating'].mode().iloc[0],
                    'std': team_data['happiness_rating'].std()
                }
            }
        
        return stats_by_team

    def perform_hypothesis_testing(self) -> Dict:
        """Perform hypothesis testing between teams"""
        df = pd.DataFrame(self.survey_data)
        
        test_results = {}
        metrics = ['day_rating', 'accomplishment_rating', 'happiness_rating']
        teams = ['Software', 'Hardware', 'Maintenance']
        
        for metric in metrics:
            test_results[metric] = {}
            for team1 in teams:
                for team2 in teams:
                    if team1 < team2:
                        t_stat, p_value = stats.ttest_ind(
                            df[df['team_type'] == team1][metric],
                            df[df['team_type'] == team2][metric]
                        )
                        test_results[metric][f'{team1}_vs_{team2}'] = {
                            't_statistic': t_stat,
                            'p_value': p_value
                        }
        
        return test_results

    def generate_visualizations(self):
        """Generate various visualizations of the survey data"""
        df = pd.DataFrame(self.survey_data)
        
        # Set up the plotting style
        plt.style.use('seaborn')
        
        # 1. Time series plot of average ratings by team
        plt.figure(figsize=(15, 8))
        for team in ['Software', 'Hardware', 'Maintenance']:
            team_data = df[df['team_type'] == team].groupby('date')['happiness_rating'].mean()
            plt.plot(team_data.index, team_data.values, label=team, linewidth=2)
        
        plt.title('Average Happiness Rating Over Time by Team')
        plt.xlabel('Date')
        plt.ylabel('Average Happiness Rating')
        plt.legend()
        plt.savefig('happiness_over_time.png')
        plt.close()
        
        # 2. Box plots for all metrics by team
        plt.figure(figsize=(15, 8))
        metrics = ['day_rating', 'accomplishment_rating', 'happiness_rating']
        
        for i, metric in enumerate(metrics, 1):
            plt.subplot(1, 3, i)
            sns.boxplot(data=df, x='team_type', y=metric)
            plt.title(f'{metric.replace("_", " ").title()}')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('ratings_distribution.png')
        plt.close()
        
        # 3. Correlation heatmap
        plt.figure(figsize=(10, 8))
        correlation_matrix = df[['day_rating', 'accomplishment_rating', 'happiness_rating']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlation between Survey Metrics')
        plt.savefig('correlation_heatmap.png')
        plt.close()

def main():
    # Initialize the survey system
    survey_system = EmployeeSurveySystem()
    
    # Generate synthetic survey data
    print("Generating yearly survey data...")
    survey_system.generate_yearly_survey_data()
    
    # Calculate descriptive statistics
    print("\nCalculating descriptive statistics...")
    stats = survey_system.calculate_descriptive_statistics()
    
    # Perform hypothesis testing
    print("\nPerforming hypothesis testing...")
    hypothesis_results = survey_system.perform_hypothesis_testing()
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    survey_system.generate_visualizations()
    
    # Save results
    results = {
        'descriptive_statistics': stats,
        'hypothesis_testing': hypothesis_results
    }
    
    with open('survey_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary statistics
    print("\nSummary Statistics by Team:")
    print("=" * 50)
    
    for team, team_stats in stats.items():
        print(f"\n{team} Team:")
        print(f"Average day rating: {team_stats['day_rating']['mean']:.2f}")
        print(f"Average accomplishment rating: {team_stats['accomplishment_rating']['mean']:.2f}")
        print(f"Average happiness rating: {team_stats['happiness_rating']['mean']:.2f}")
        print(f"Happiness standard deviation: {team_stats['happiness_rating']['std']:.2f}")

    print("\nAnalysis complete! Check the following files for results:")
    print("1. survey_analysis_results.json - Detailed statistical analysis")
    print("2. happiness_over_time.png - Time series plot of happiness ratings")
    print("3. ratings_distribution.png - Distribution of ratings by team")
    print("4. correlation_heatmap.png - Correlation between survey metrics")

if __name__ == "__main__":
    main()
