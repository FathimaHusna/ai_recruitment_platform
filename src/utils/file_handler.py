import json
from typing import List, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

class FileHandler:
    """Handle file operations for job descriptions."""
    def save_to_json(self, data: Any, filename: str) -> None:
        """Save data to a JSON file."""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved data to {filename}")
        except Exception as e:
            logger.error(f"Error saving to {filename}: {e}")
            raise

    def generate_summary_report(self, job_descriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary report from job descriptions."""
        try:
            categories = {}
            for jd in job_descriptions:
                category = jd.get('category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1

            summary = {
                'total_jobs': len(job_descriptions),
                'categories': categories
            }
            return summary
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            raise