import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import re
from typing import Dict, List, Optional
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import time
from collections import Counter

class BotRequirementsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.logger = self._setup_logger()
        self.results = []

    def _setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot_scraper.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def extract_project_duration(self, text: str) -> Optional[int]:
        """Extract project duration in months from text."""
        duration_patterns = [
            r'(\d+)\s*months?',
            r'(\d+)\s*weeks?',
            r'(\d+)\s*years?'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text.lower())
            if match:
                value = int(match.group(1))
                if 'year' in pattern:
                    return value * 12
                elif 'week' in pattern:
                    return round(value / 4)
                return value
        return None

    def extract_requirements(self, text: str) -> List[str]:
        """Extract requirements from text using improved pattern matching."""
        requirements = []
        
        # Common requirement patterns
        requirement_patterns = [
            r'(?:Prerequisites?|Requirements?):?\s*(.*?)(?:\n|$)',
            r'(?:This sample|The bot) (?:requires|needs)\s*(.*?)(?:\n|$)',
            r'(?:You will need|You\'ll need)\s*(.*?)(?:\n|$)',
            r'(?:Must|Should|Needs to|Required to)\s*(.*?)(?:\n|$)',
            r'(?:The following are required|The following is required):?\s*(.*?)(?:\n|$)',
            r'(?:To run this sample|To use this bot)\s*(.*?)(?:\n|$)',
            r'(?:Before running|Before using)\s*(.*?)(?:\n|$)',
            r'(?:This demonstrates|This shows how to)\s*(.*?)(?:\n|$)',
            r'(?:Key features|Features):?\s*(.*?)(?:\n|$)',
            r'(?:Capabilities|Functions):?\s*(.*?)(?:\n|$)'
        ]
        
        # Extract requirements using patterns
        for pattern in requirement_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                req = match.group(1).strip()
                if req and len(req) > 10:  # Filter out very short matches
                    requirements.append(req)
        
        # Look for bullet points that might indicate requirements
        bullet_points = re.findall(r'(?:^|\n)\s*[-*•]\s*(.*?)(?:\n|$)', text)
        for point in bullet_points:
            if len(point.strip()) > 10:  # Filter out very short points
                requirements.append(point.strip())
        
        # Extract sentences that might indicate requirements
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in ['must', 'should', 'need', 'require', 'important', 'necessary']):
                if len(sentence) > 10:  # Filter out very short sentences
                    requirements.append(sentence)
        
        return list(set(requirements))  # Remove duplicates

    def scrape_project_data(self, url: str) -> Dict:
        """Scrape project data from a given URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Focus on README content
            readme_content = soup.find('article', class_='markdown-body')
            if not readme_content:
                readme_content = soup.find('div', id='readme')
            
            if readme_content:
                text_content = readme_content.get_text()
            else:
                text_content = soup.get_text()
            
            # Extract project information
            project_data = {
                'url': url,
                'title': self._extract_title(soup),
                'requirements': self.extract_requirements(text_content),
                'duration_months': self.extract_project_duration(text_content),
                'scraped_at': datetime.now().isoformat(),
                'success_indicators': self._extract_success_indicators(text_content)
            }
            
            # Add repository metadata
            metadata = self._extract_repo_metadata(soup)
            if metadata:
                project_data.update(metadata)
            
            self.logger.info(f"Successfully scraped data from {url}")
            return project_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract clean project title."""
        title = soup.find('h1', class_='h1')
        if title:
            return title.get_text().strip()
        return soup.title.string if soup.title else "Unknown Title"

    def _extract_repo_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract repository metadata."""
        metadata = {}
        
        # Extract stars count
        stars_element = soup.find('a', href=lambda x: x and x.endswith('/stargazers'))
        if stars_element:
            stars_text = stars_element.get_text().strip()
            try:
                metadata['stars'] = int(''.join(filter(str.isdigit, stars_text)))
            except ValueError:
                pass

        # Extract last update time
        time_element = soup.find('relative-time')
        if time_element:
            metadata['last_updated'] = time_element.get('datetime')

        # Extract language stats
        languages = {}
        lang_stats = soup.find_all('div', class_='BorderGrid-cell')
        for stat in lang_stats:
            lang_name = stat.find('span', class_='color-fg-default')
            if lang_name:
                lang_percent = stat.find('span', class_='color-fg-muted')
                if lang_percent:
                    languages[lang_name.text.strip()] = lang_percent.text.strip()
        
        if languages:
            metadata['languages'] = languages

        return metadata

    def _extract_success_indicators(self, text: str) -> List[str]:
        """Extract success indicators from text using improved pattern matching."""
        indicators = []
        
        # Success indicator patterns
        success_patterns = [
            r'(?:Successfully|Successfully implemented|Completed)\s*(.*?)(?:\n|$)',
            r'(?:Improved|Enhanced|Optimized)\s*(.*?)(?:\n|$)',
            r'(?:Benefits?|Advantages?):?\s*(.*?)(?:\n|$)',
            r'(?:This solution|This approach)\s*(.*?)(?:\n|$)',
            r'(?:Results in|Leads to|Enables)\s*(.*?)(?:\n|$)',
            r'(?:Performance|Efficiency|Effectiveness):?\s*(.*?)(?:\n|$)',
            r'(?:Key achievements?|Major improvements?):?\s*(.*?)(?:\n|$)',
            r'(?:Positive outcomes?|Success metrics?):?\s*(.*?)(?:\n|$)',
            r'(?:This demonstrates|This shows)\s*(.*?)(?:\n|$)',
            r'(?:Features|Capabilities):?\s*(.*?)(?:\n|$)'
        ]
        
        # Extract success indicators using patterns
        for pattern in success_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                indicator = match.group(1).strip()
                if indicator and len(indicator) > 10:  # Filter out very short matches
                    indicators.append(indicator)
        
        # Look for bullet points that might indicate success
        bullet_points = re.findall(r'(?:^|\n)\s*[-*•]\s*(.*?)(?:\n|$)', text)
        for point in bullet_points:
            if any(keyword in point.lower() for keyword in ['success', 'improve', 'benefit', 'achieve', 'complete']):
                if len(point.strip()) > 10:  # Filter out very short points
                    indicators.append(point.strip())
        
        # Extract sentences that might indicate success
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in ['success', 'improve', 'benefit', 'achieve', 'complete', 'better', 'faster']):
                if len(sentence) > 10:  # Filter out very short sentences
                    indicators.append(sentence)
        
        return list(set(indicators))  # Remove duplicates

    def categorize_requirements(self, requirements):
        """Categorize requirements into meaningful groups."""
        categories = {
            'setup': [],
            'core_features': [],
            'advanced_features': [],
            'integration': [],
            'security': [],
            'performance': [],
            'user_experience': [],
            'development': []
        }
        
        # Keywords for each category
        categorization = {
            'setup': ['install', 'prerequisite', 'environment', 'setup', 'configure', 'dependencies'],
            'core_features': ['basic', 'core', 'essential', 'fundamental', 'primary', 'main'],
            'advanced_features': ['advanced', 'complex', 'sophisticated', 'additional', 'extended'],
            'integration': ['integrate', 'connect', 'api', 'external', 'third-party', 'service'],
            'security': ['security', 'authentication', 'authorization', 'credential', 'token', 'protect'],
            'performance': ['performance', 'speed', 'efficient', 'optimize', 'scale', 'responsive'],
            'user_experience': ['user', 'interface', 'experience', 'ui', 'ux', 'interaction'],
            'development': ['develop', 'code', 'implement', 'build', 'test', 'debug']
        }
        
        for req in requirements:
            req_lower = req.lower()
            categorized = False
            
            # Check each category's keywords
            for category, keywords in categorization.items():
                if any(keyword in req_lower for keyword in keywords):
                    categories[category].append(req)
                    categorized = True
                    break
            
            # If not categorized, try to intelligently categorize based on content
            if not categorized:
                if any(word in req_lower for word in ['dialog', 'conversation', 'message', 'chat']):
                    categories['core_features'].append(req)
                elif any(word in req_lower for word in ['state', 'store', 'data', 'persistence']):
                    categories['advanced_features'].append(req)
                elif any(word in req_lower for word in ['deploy', 'cloud', 'azure', 'host']):
                    categories['integration'].append(req)
                else:
                    # Default to development if no other category fits
                    categories['development'].append(req)
        
        return categories

    def analyze_results(self):
        """Analyze and summarize the scraped results."""
        all_requirements = []
        all_success_indicators = []
        all_durations = []
        
        for project in self.results:  # self.results is already the projects list
            all_requirements.extend(project['requirements'])
            all_success_indicators.extend(project['success_indicators'])
            if project['duration_months']:
                all_durations.append(project['duration_months'])
        
        # Categorize requirements
        categorized_reqs = self.categorize_requirements(all_requirements)
        
        return {
            'total_projects': len(self.results),
            'avg_duration_months': sum(all_durations) / len(all_durations) if all_durations else None,
            'avg_requirements': len(all_requirements) / len(self.results) if self.results else 0,
            'requirements_by_category': categorized_reqs,
            'common_requirements': list(set(all_requirements)),
            'success_patterns': dict(Counter(all_success_indicators))
        }

    def save_results(self, filename: str = 'bot_requirements_analysis.json'):
        """Save scraped results to a JSON file."""
        output = {
            'projects': self.results,
            'summary': self.analyze_results()
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        # Also save as CSV for easy viewing
        df = pd.DataFrame(self.results)
        df.to_csv('bot_requirements_analysis.csv', index=False)
        
        self.logger.info(f"Results saved to {filename} and bot_requirements_analysis.csv")

    def scrape_multiple_sources(self, urls: List[str], max_workers: int = 5):
        """Scrape multiple URLs concurrently."""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.scrape_project_data, urls))
            self.results.extend([r for r in results if r])

if __name__ == "__main__":
    # Example usage
    scraper = BotRequirementsScraper()
    
    # Test URLs focusing on well-documented bot projects with clear requirements
    target_urls = [
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/02.echo-bot",
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/13.core-bot",
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/45.state-management",
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/16.proactive-messages",
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/44.prompt-for-user-input",
        "https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/24.bot-authentication-msgraph"
    ]
    
    print("Starting bot requirements analysis...")
    print("This may take a few minutes as we analyze each project in detail...")
    
    scraper.scrape_multiple_sources(target_urls)
    scraper.save_results()
    
    # Print a quick summary
    print("\nAnalysis complete! Summary of findings:")
    print("-" * 50)
    
    with open('bot_requirements_analysis.json', 'r') as f:
        data = json.load(f)
        summary = data.get('summary', {})
        
        if summary.get('total_projects'):
            print(f"Total projects analyzed: {summary['total_projects']}")
        if summary.get('avg_duration_months'):
            print(f"Average development time: {summary['avg_duration_months']:.1f} months")
        if summary.get('avg_requirements'):
            print(f"Average requirements per project: {summary['avg_requirements']:.1f}")
        
        print("\nCommon Requirements:")
        for req in summary.get('common_requirements', [])[:5]:
            print(f"- {req}")
            
        print("\nDetailed results saved to:")
        print("- bot_requirements_analysis.json")
        print("- bot_requirements_analysis.csv")
