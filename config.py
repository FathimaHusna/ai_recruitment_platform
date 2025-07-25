# config.py
from typing import Dict, List

class JobConfig:
    """Configuration for job description generation."""
    JOB_CATEGORIES: Dict[str, List[str]] = {
        "Software Engineering": [
            "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Senior Frontend Developer", "Senior Backend Developer", 
            "Lead Full Stack Developer", "Software Engineer", "Senior Software Engineer"
        ],
        "Data Science": [
            "Data Scientist", "Data Analyst", "Senior Data Scientist",
            "Database Administrator", "Business Intelligence Analyst",
            "Data Engineer", "Junior Data Analyst", "Principal Data Scientist"
        ],
        "DevOps": [
            "DevOps Engineer", "Site Reliability Engineer", "Cloud Specialist",
            "Senior DevOps Engineer", "Cloud Architect", "Infrastructure Engineer",
            "Platform Engineer", "Release Engineer"
        ],
        "Machine Learning": [
            "Machine Learning Engineer", "AI Researcher", "NLP Specialist",
            "Senior ML Engineer", "Computer Vision Engineer", "AI/ML Consultant",
            "Deep Learning Engineer", "MLOps Engineer"
        ],
        "Quality Assurance": [
            "QA Engineer", "Test Automation Specialist", "QA Manager",
            "Senior QA Engineer", "Performance Test Engineer", "QA Lead",
            "Manual Testing Specialist", "Test Architect"
        ],
        "Project Management": [
            "Project Manager", "Scrum Master", "Product Owner",
            "Senior Project Manager", "Technical Project Manager", "Agile Coach",
            "Program Manager", "Product Manager"
        ],
        "Business Analytics": [
            "Business Analyst", "BI Specialist", "Data Visualization Expert",
            "Senior Business Analyst", "Business Intelligence Developer",
            "Analytics Consultant", "Reporting Analyst", "Market Research Analyst"
        ]
    }

    COMPANY_TYPES: List[str] = [
        "Tech Startup", "Fortune 500 Company", "Consulting Firm", "Healthcare Organization",
        "Financial Services", "E-commerce Platform", "SaaS Company", "Manufacturing Company",
        "Government Agency", "Non-profit Organization", "Educational Institution", "Media Company"
    ]

    LOCATIONS: List[str] = [
        "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", 
        "Boston, MA", "Chicago, IL", "Denver, CO", "Remote", "Atlanta, GA",
        "Los Angeles, CA", "Portland, OR", "Miami, FL", "Phoenix, AZ",
        "Dallas, TX", "Washington, DC", "San Diego, CA"
    ]

    EXPERIENCE_LEVELS: List[str] = ["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"]