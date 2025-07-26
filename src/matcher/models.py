from dataclasses import dataclass
from typing import List

@dataclass
class ProcessedResume:
    """Data class for processed resume information"""
    name: str
    email: str
    phone: str
    location: str
    summary: str
    experience_years: str
    education: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    work_experience: List[str]
    certifications: List[str]
    keywords: List[str]
    resume_text: str
    processed_at: str

@dataclass
class JobMatch:
    """Data class for job matching results"""
    job_id: str
    title: str
    category: str
    company_type: str
    location: str
    similarity_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    job_summary: str
    salary_range: str
    match_reasons: List[str]