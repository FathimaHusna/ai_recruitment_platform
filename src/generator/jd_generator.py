# jd_generator.py
import random
import time
from typing import List, Dict, Optional
from datetime import datetime
from src.generator.config import JobConfig
from src.utils.api_client import OpenAIClient

class JobDescriptionGenerator:
    """Generates job descriptions."""
    
    def __init__(self, api_client: OpenAIClient):
        self.api_client = api_client
        self.config = JobConfig()

    def generate_job_description_prompt(self, role: str, category: str, company_type: str, 
                                      location: str, experience_level: str) -> str:
        """Create a prompt for generating job descriptions."""
        return f"""
        Generate a realistic and detailed job description for the following position:

        Job Title: {role}
        Category: {category}
        Company Type: {company_type}
        Location: {location}
        Experience Level: {experience_level}

        Please include the following sections in a professional format:
        1. **Job Title**: {role}
        2. **Company Overview**: Brief description of the company (2-3 sentences)
        3. **Job Summary**: Overview of the role and its importance (3-4 sentences)
        4. **Key Responsibilities**: 5-7 specific responsibilities
        5. **Required Qualifications**: 
            - Education requirements
            - Years of experience
            - Technical skills (be specific to the role)
            - Soft skills
        6. **Preferred Qualifications**: 2-3 nice-to-have skills or experiences
        7. **Benefits**: 3-4 attractive benefits
        8. **Location**: {location}
        9. **Employment Type**: Full-time
        10. **Salary Range**: Provide a realistic range based on the role and location

        Make the job description engaging, realistic, and tailored to the specific role and industry.
        Use professional language but keep it approachable.
        """

    def generate_single_jd(self, role: str, category: str, company_type: str = None, 
                          location: str = None, experience_level: str = None) -> Optional[Dict]:
        """Generate a single job description."""
        company_type = company_type or random.choice(self.config.COMPANY_TYPES)
        location = location or random.choice(self.config.LOCATIONS)
        experience_level = experience_level or random.choice(self.config.EXPERIENCE_LEVELS)
        
        if category not in self.config.JOB_CATEGORIES:
            print(f"Error: Invalid category. Choose from {list(self.config.JOB_CATEGORIES.keys())}")
            return None
        if role not in self.config.JOB_CATEGORIES[category]:
            print(f"Error: Invalid role for {category}. Choose from {self.config.JOB_CATEGORIES[category]}")
            return None
        if company_type not in self.config.COMPANY_TYPES:
            print(f"Error: Invalid company type. Choose from {self.config.COMPANY_TYPES}")
            return None
        if location not in self.config.LOCATIONS:
            print(f"Error: Invalid location. Choose from {self.config.LOCATIONS}")
            return None
        if experience_level not in self.config.EXPERIENCE_LEVELS:
            print(f"Error: Invalid experience level. Choose from {self.config.EXPERIENCE_LEVELS}")
            return None

        prompt = self.generate_job_description_prompt(role, category, company_type, location, experience_level)
        raw_jd = self.api_client.generate_text(prompt, context="You are an expert HR professional and job description writer.")
        
        if not raw_jd:
            return None

        return {
            "id": f"JD_{random.randint(1000, 9999)}_{int(time.time())}",
            "title": role,
            "category": category,
            "company_type": company_type,
            "location": location,
            "experience_level": experience_level,
            "full_description": raw_jd,
            "generated_at": datetime.now().isoformat(),
            "status": "active"
        }

    def generate_all_job_descriptions(self, num_descriptions: int) -> List[Dict]:
        """Generate multiple job descriptions."""
        job_descriptions = []
        batch_size = 10
        for i in range(0, num_descriptions, batch_size):
            print(f"Processing batch {i//batch_size + 1}/{(num_descriptions-1)//batch_size + 1}")
            for j in range(min(batch_size, num_descriptions - i)):
                category = random.choice(list(self.config.JOB_CATEGORIES.keys()))
                role = random.choice(self.config.JOB_CATEGORIES[category])
                print(f"Generating job description {i+j+1}/{num_descriptions}: {role} ({category})")
                jd = self.generate_single_jd(role, category)
                if jd:
                    job_descriptions.append(jd)
                time.sleep(1)
            time.sleep(10)
        print(f"Generated {len(job_descriptions)} job descriptions successfully!")
        return job_descriptions