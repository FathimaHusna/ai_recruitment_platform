import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
from .models import ProcessedResume, JobMatch

logger = logging.getLogger(__name__)

class RAGJobMatcher:
    """RAG-based job matching system"""
    
    def __init__(self, openai_api_key: str, mongo_uri: str, database_name: str):
        """Initialize the RAG job matcher"""
        self.client = openai.OpenAI(api_key=openai_api_key)
        retries = 3
        for attempt in range(retries):
            try:
                self.mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                self.mongo_client.admin.command("ping")  # Test connection
                self.db = self.mongo_client[database_name]
                self.collection = self.db.job_descriptions
                logger.info("Connected to MongoDB Atlas successfully")
                break
            except ConnectionFailure as e:
                logger.error(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt == retries - 1:
                    raise
        
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 3),
            lowercase=True
        )
        self.job_vectors = None
        self.job_documents = []

    def _extract_strings(self, field):
        """Helper to extract strings from a list of strings or dicts."""
        if isinstance(field, list):
            if field and isinstance(field[0], dict):
                # Try 'name' key, fallback to first value
                return [str(item.get('name', next(iter(item.values()), ''))) for item in field]
            return [str(item) for item in field]
        return []

    def load_and_vectorize_jobs(self):
        """Load jobs from MongoDB and create TF-IDF vectors"""
        try:
            jobs = list(self.collection.find({}, {"_id": 0}))
            if not jobs:
                st.error("No jobs found in database. Please run Task 2 first.")
                return False
            
            self.job_documents = []
            for job in jobs:
                job_text = f"""
                {job.get('title', '')} {job.get('category', '')} 
                {' '.join(self._extract_strings(job.get('technical_skills', [])))}
                {' '.join(self._extract_strings(job.get('soft_skills', [])))}
                {' '.join(self._extract_strings(job.get('responsibilities', [])))}
                {' '.join(self._extract_strings(job.get('keywords', [])))}
                {job.get('job_summary', '')}
                """.strip()
                
                self.job_documents.append({
                    'job_data': job,
                    'text': job_text
                })
            
            job_texts = [doc['text'] for doc in self.job_documents]
            self.job_vectors = self.vectorizer.fit_transform(job_texts)
            logger.info(f"Loaded and vectorized {len(jobs)} jobs")
            return True
            
        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            st.error(f"Error loading jobs from database: {e}")
            return False
        
    # def load_and_vectorize_jobs(self):
    #     """Load jobs from MongoDB and create TF-IDF vectors"""
    #     try:
    #         jobs = list(self.collection.find({}, {"_id": 0}))
    #         if not jobs:
    #             st.error("No jobs found in database. Please run Task 2 first.")
        #         return False
            
        #     self.job_documents = []
        #     for job in jobs:
        #         job_text = f"""
        #         {job.get('title', '')} {job.get('category', '')} 
        #         {' '.join(job.get('technical_skills', []))} 
        #         {' '.join(job.get('soft_skills', []))} 
        #         {' '.join(job.get('responsibilities', []))} 
        #         {' '.join(job.get('keywords', []))}
        #         {job.get('job_summary', '')}
        #         """.strip()
                
        #         self.job_documents.append({
        #             'job_data': job,
        #             'text': job_text
        #         })
            
        #     job_texts = [doc['text'] for doc in self.job_documents]
        #     self.job_vectors = self.vectorizer.fit_transform(job_texts)
        #     logger.info(f"Loaded and vectorized {len(jobs)} jobs")
        #     return True
            
        # except Exception as e:
        #     logger.error(f"Error loading jobs: {e}")
        #     st.error(f"Error loading jobs from database: {e}")
        #     return False
    
    def process_resume_with_llm(self, resume_text: str) -> Optional[ProcessedResume]:
        """Process resume using LLM to extract structured information"""
        try:
            prompt = f"""
            Analyze the following resume and extract structured information. 
            Return the information in JSON format with the following exact keys:

            Resume Text:
            {resume_text}

            Extract and return JSON with these keys:
            {{
                "name": "full name of the person",
                "email": "email address",
                "phone": "phone number",
                "location": "city, state or location",
                "summary": "professional summary or objective",
                "experience_years": "total years of experience or estimate",
                "education": ["degree", "university", "certifications"],
                "technical_skills": ["programming languages", "tools", "technologies"],
                "soft_skills": ["communication", "leadership", "teamwork"],
                "work_experience": ["job titles", "companies", "key achievements"],
                "certifications": ["professional certifications", "licenses"],
                "keywords": ["relevant keywords for job matching"]
            }}

            Guidelines:
            - Extract only information that is explicitly mentioned
            - For technical_skills, focus on hard skills, tools, and technologies
            - For keywords, include important terms that would help in job matching
            - If information is not available, use empty array [] or "Not specified"
            - Return only valid JSON, no additional text
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume parser. Extract structured information and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            extracted_text = response.choices[0].message.content.strip()
            start_idx = extracted_text.find('{')
            end_idx = extracted_text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                extracted_text = extracted_text[start_idx:end_idx + 1]
            
            extracted_data = json.loads(extracted_text)
            
            processed_resume = ProcessedResume(
                name=extracted_data.get('name', 'Not specified'),
                email=extracted_data.get('email', 'Not specified'),
                phone=extracted_data.get('phone', 'Not specified'),
                location=extracted_data.get('location', 'Not specified'),
                summary=extracted_data.get('summary', ''),
                experience_years=extracted_data.get('experience_years', 'Not specified'),
                education=extracted_data.get('education', []),
                technical_skills=extracted_data.get('technical_skills', []),
                soft_skills=extracted_data.get('soft_skills', []),
                work_experience=extracted_data.get('work_experience', []),
                certifications=extracted_data.get('certifications', []),
                keywords=extracted_data.get('keywords', []),
                resume_text=resume_text,
                processed_at=datetime.now().isoformat()
            )
            
            return processed_resume
            
        except Exception as e:
            logger.error(f"Error processing resume with LLM: {e}")
            return None
    
    def find_matching_jobs(self, processed_resume: ProcessedResume, top_k: int = 10) -> List[JobMatch]:
        """Find matching jobs using RAG approach"""
        try:
            if self.job_vectors is None:
                if not self.load_and_vectorize_jobs():
                    return []
            
            resume_text = f"""
            {processed_resume.summary}
            {' '.join(self._extract_strings(processed_resume.technical_skills))}
            {' '.join(self._extract_strings(processed_resume.soft_skills))}
            {' '.join(self._extract_strings(processed_resume.work_experience))}
            {' '.join(self._extract_strings(processed_resume.keywords))}
            """
            
            resume_vector = self.vectorizer.transform([resume_text])
            similarities = cosine_similarity(resume_vector, self.job_vectors).flatten()
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            matches = []
            for idx in top_indices:
                job_data = self.job_documents[idx]['job_data']
                similarity_score = similarities[idx]
                
                resume_skills = set([skill.lower() for skill in self._extract_strings(processed_resume.technical_skills)])
                job_skills = set([skill.lower() for skill in self._extract_strings(job_data.get('technical_skills', []))])
                
                matching_skills = list(resume_skills.intersection(job_skills))
                missing_skills = list(job_skills.difference(resume_skills))
                
                match_reasons = self._generate_match_reasons(
                    processed_resume, job_data, similarity_score, matching_skills
                )
                
                match = JobMatch(
                    job_id=job_data.get('job_id', ''),
                    title=job_data.get('title', ''),
                    category=job_data.get('category', ''),
                    company_type=job_data.get('company_type', ''),
                    location=job_data.get('location', ''),
                    similarity_score=similarity_score,
                    matching_skills=matching_skills,
                    missing_skills=missing_skills[:5],
                    job_summary=job_data.get('job_summary', ''),
                    salary_range=job_data.get('salary_range', 'Not specified'),
                    match_reasons=match_reasons
                )
                
                matches.append(match)
            
            return matches
            
        except Exception as e:
            logger.error(f"Error finding matching jobs: {e}")
            return []
    def _generate_match_reasons(self, resume: ProcessedResume, job: Dict, 
                              similarity_score: float, matching_skills: List[str]) -> List[str]:
        """Generate human-readable match reasons"""
        reasons = []
        if similarity_score > 0.3:
            reasons.append(f"High compatibility score ({similarity_score:.2%})")
        if matching_skills:
            skill_str = ', '.join(matching_skills[:3])
            reasons.append(f"Matching skills: {skill_str}")
        resume_keywords = [kw.lower() for kw in resume.keywords]
        job_category = job.get('category', '').lower()
        if any(keyword in job_category for keyword in resume_keywords):
            reasons.append(f"Relevant experience in {job.get('category', '')}")
        if resume.location.lower() in job.get('location', '').lower():
            reasons.append("Location preference match")
        return reasons[:4]