# file_handler.py
import json
from typing import List, Dict
from datetime import datetime

class FileHandler:
    """Handles saving job descriptions and summary reports to JSON files."""
    
    @staticmethod
    def save_to_json(data: List[Dict], filename: str = "job_descriptions.json"):
        """Save data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def generate_summary_report(job_descriptions: List[Dict]) -> Dict:
        """Generate a summary report of the generated job descriptions."""
        if not job_descriptions:
            return {}
        
        category_counts = {}
        location_counts = {}
        experience_counts = {}
        company_type_counts = {}
        
        for jd in job_descriptions:
            category = jd.get('category', 'Unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
            location = jd.get('location', 'Unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
            exp_level = jd.get('experience_level', 'Unknown')
            experience_counts[exp_level] = experience_counts.get(exp_level, 0) + 1
            company_type = jd.get('company_type', 'Unknown')
            company_type_counts[company_type] = company_type_counts.get(company_type, 0) + 1
        
        return {
            "total_jobs": len(job_descriptions),
            "categories": category_counts,
            "locations": location_counts,
            "experience_levels": experience_counts,
            "company_types": company_type_counts,
            "generation_date": datetime.now().isoformat()
        }