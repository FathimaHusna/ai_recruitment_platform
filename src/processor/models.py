from dataclasses import dataclass
from typing import List

@dataclass
class ProcessedJobDescription:
    """Data class for structured job description"""
    job_id: str
    title: str
    category: str
    company_type: str
    location: str
    employment_type: str
    experience_level: str
    education_requirements: List[str]
    years_of_experience: str
    technical_skills: List[str]
    soft_skills: List[str]
    responsibilities: List[str]
    required_qualifications: List[str]
    preferred_qualifications: List[str]
    benefits: List[str]
    salary_range: str
    job_summary: str
    company_overview: str
    original_description: str
    processed_at: str
    keywords: List[str]
    seniority_level: int  # 1=Entry, 2=Mid, 3=Senior, 4=Lead/Principal