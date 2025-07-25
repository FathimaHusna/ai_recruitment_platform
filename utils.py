# utils.py
from typing import Optional, Dict
from api_client import OpenAIClient

def validate_inputs(role: str, category: str, company_type: str, location: str, 
                   experience_level: str, config: 'JobConfig') -> bool:
    """Validate inputs against configuration."""
    if category not in config.JOB_CATEGORIES:
        print(f"Error: Invalid category. Choose from {list(config.JOB_CATEGORIES.keys())}")
        return False
    if role not in config.JOB_CATEGORIES[category]:
        print(f"Error: Invalid role for {category}. Choose from {config.JOB_CATEGORIES[category]}")
        return False
    if company_type not in config.COMPANY_TYPES:
        print(f"Error: Invalid company type. Choose from {config.COMPANY_TYPES}")
        return False
    if location not in config.LOCATIONS:
        print(f"Error: Invalid location. Choose from {config.LOCATIONS}")
        return False
    if experience_level not in config.EXPERIENCE_LEVELS:
        print(f"Error: Invalid experience level. Choose from {config.EXPERIENCE_LEVELS}")
        return False
    return True