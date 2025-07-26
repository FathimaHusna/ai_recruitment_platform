import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dataclasses import asdict
import time
from .models import ProcessedJobDescription
from .utils import clean_json_response, map_seniority_level
import certifi

# Set up logging
logger = logging.getLogger(__name__)

class JobDescriptionProcessor:
    def __init__(self, openai_api_key: str, mongo_uri: str, 
                 database_name: str = "recruitment_platform"):
        """
        Initialize the Job Description Processor
        
        Args:
            openai_api_key (str): OpenAI API key
            mongo_uri (str): MongoDB connection URI
            database_name (str): Database name
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        
        # MongoDB setup with retry logic
        retries = 3
        for attempt in range(retries):
            try:
                self.mongo_client = MongoClient(mongo_uri,
                                                 serverSelectionTimeoutMS=5000,
                                                  tlsCAFile=certifi.where(),
                                                  tlsAllowInvalidCertificates=False)
                self.mongo_client.admin.command("ping")  # Test connection
                self.db = self.mongo_client[database_name]
                self.collection = self.db.job_descriptions
                
                # Create indexes for better query performance
                self.collection.create_index("job_id", unique=True)
                self.collection.create_index("title")
                self.collection.create_index("category")
                self.collection.create_index("location")
                self.collection.create_index("technical_skills")
                self.collection.create_index("keywords")
                self.collection.create_index("seniority_level")
                
                logger.info("Connected to MongoDB Atlas successfully")
                break
            except ConnectionFailure as e:
                logger.error(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(5)

    def create_extraction_prompt(self, job_description: str) -> str:
        """
        Create a detailed prompt for extracting structured information from job descriptions
        
        Args:
            job_description (str): Raw job description text
            
        Returns:
            str: Formatted extraction prompt
        """
        prompt = f"""
        Analyze the following job description and extract structured information. 
        Return the information in JSON format with the following exact keys:

        Job Description:
        {job_description}

        Extract and return JSON with these keys:
        {{
            "title": "exact job title",
            "job_summary": "brief 2-3 sentence summary of the role",
            "company_overview": "company description if available",
            "responsibilities": ["list", "of", "key", "responsibilities"],
            "education_requirements": ["degree requirements", "certifications"],
            "years_of_experience": "X-Y years or specific requirement",
            "technical_skills": ["specific", "technical", "skills", "tools", "technologies"],
            "soft_skills": ["communication", "leadership", "teamwork", "etc"],
            "required_qualifications": ["must", "have", "qualifications"],
            "preferred_qualifications": ["nice", "to", "have", "qualifications"],
            "benefits": ["list", "of", "benefits", "mentioned"],
            "salary_range": "salary range if mentioned or 'Not specified'",
            "employment_type": "Full-time, Part-time, Contract, etc.",
            "keywords": ["relevant", "keywords", "for", "search", "matching"]
        }}

        Guidelines:
        - Extract only information that is explicitly mentioned
        - For technical_skills, include programming languages, frameworks, tools, databases, etc.
        - For keywords, include important terms that would help in job matching
        - Keep lists concise but comprehensive
        - If information is not available, use empty array [] or "Not specified"
        - Return only valid JSON, no additional text
        """
        return prompt

    def extract_structured_data(self, raw_jd: Dict) -> Optional[ProcessedJobDescription]:
        """
        Extract structured data from a raw job description using LLM
        
        Args:
            raw_jd (Dict): Raw job description data
            
        Returns:
            Optional[ProcessedJobDescription]: Processed job description or None if failed
        """
        try:
            full_description = raw_jd.get('full_description', '')
            prompt = self.create_extraction_prompt(full_description)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR data analyst. Extract structured information from job descriptions and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            extracted_text = response.choices[0].message.content.strip()
            extracted_text = clean_json_response(extracted_text)
            extracted_data = json.loads(extracted_text)
            
            seniority_level = map_seniority_level(raw_jd.get('experience_level', ''))
            
            processed_jd = ProcessedJobDescription(
                job_id=raw_jd.get('id', f"JD_{int(time.time())}"),
                title=extracted_data.get('title', raw_jd.get('title', 'Unknown')),
                category=raw_jd.get('category', 'Unknown'),
                company_type=raw_jd.get('company_type', 'Unknown'),
                location=raw_jd.get('location', 'Unknown'),
                employment_type=extracted_data.get('employment_type', 'Full-time'),
                experience_level=raw_jd.get('experience_level', 'Not specified'),
                education_requirements=extracted_data.get('education_requirements', []),
                years_of_experience=extracted_data.get('years_of_experience', 'Not specified'),
                technical_skills=extracted_data.get('technical_skills', []),
                soft_skills=extracted_data.get('soft_skills', []),
                responsibilities=extracted_data.get('responsibilities', []),
                required_qualifications=extracted_data.get('required_qualifications', []),
                preferred_qualifications=extracted_data.get('preferred_qualifications', []),
                benefits=extracted_data.get('benefits', []),
                salary_range=extracted_data.get('salary_range', 'Not specified'),
                job_summary=extracted_data.get('job_summary', ''),
                company_overview=extracted_data.get('company_overview', ''),
                original_description=full_description,
                processed_at=datetime.now().isoformat(),
                keywords=extracted_data.get('keywords', []),
                seniority_level=seniority_level
            )
            
            return processed_jd
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error for job {raw_jd.get('id', 'unknown')}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing job {raw_jd.get('id', 'unknown')}: {e}")
            return None

    def store_in_mongodb(self, processed_jd: ProcessedJobDescription) -> bool:
        """
        Store processed job description in MongoDB
        
        Args:
            processed_jd (ProcessedJobDescription): Processed job description
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            jd_dict = asdict(processed_jd)
            result = self.collection.replace_one(
                {"job_id": processed_jd.job_id},
                jd_dict,
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.info(f"Successfully stored job: {processed_jd.job_id}")
                return True
            else:
                logger.warning(f"No changes made for job: {processed_jd.job_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error storing job {processed_jd.job_id} in MongoDB: {e}")
            return False

    def process_all_job_descriptions(self, input_file: str = "job_descriptions_dataset.json") -> Dict[str, Any]:
        """
        Process all job descriptions from the input file
        
        Args:
            input_file (str): Path to the job descriptions JSON file
            
        Returns:
            Dict[str, Any]: Processing results summary
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_job_descriptions = json.load(f)
            
            logger.info(f"Loaded {len(raw_job_descriptions)} job descriptions")
            
            successful_processed = 0
            failed_processed = 0
            successful_stored = 0
            failed_stored = 0
            
            for i, raw_jd in enumerate(raw_job_descriptions, 1):
                logger.info(f"Processing job {i}/{len(raw_job_descriptions)}: {raw_jd.get('title', 'Unknown')}")
                
                processed_jd = self.extract_structured_data(raw_jd)
                
                if processed_jd:
                    successful_processed += 1
                    if self.store_in_mongodb(processed_jd):
                        successful_stored += 1
                    else:
                        failed_stored += 1
                else:
                    failed_processed += 1
                    logger.error(f"Failed to process job: {raw_jd.get('id', 'unknown')}")
                
                time.sleep(1)
            
            summary = {
                "total_jobs": len(raw_job_descriptions),
                "successful_processed": successful_processed,
                "failed_processed": failed_processed,
                "successful_stored": successful_stored,
                "failed_stored": failed_stored,
                "processing_date": datetime.now().isoformat(),
                "mongodb_collection": self.collection.name,
                "mongodb_database": self.db.name
            }
            
            logger.info(f"Processing complete! Summary: {summary}")
            return summary
            
        except FileNotFoundError:
            logger.error(f"Input file {input_file} not found")
            raise
        except Exception as e:
            logger.error(f"Error processing job descriptions: {e}")
            raise

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the stored job descriptions
        
        Returns:
            Dict[str, Any]: Collection statistics
        """
        try:
            total_jobs = self.collection.count_documents({})
            category_stats = list(self.collection.aggregate([
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]))
            location_stats = list(self.collection.aggregate([
                {"$group": {"_id": "$location", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]))
            seniority_stats = list(self.collection.aggregate([
                {"$group": {"_id": "$seniority_level", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]))
            top_skills = list(self.collection.aggregate([
                {"$unwind": "$technical_skills"},
                {"$group": {"_id": "$technical_skills", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 20}
            ]))
            
            stats = {
                "total_jobs": total_jobs,
                "category_distribution": {item["_id"]: item["count"] for item in category_stats},
                "location_distribution": {item["_id"]: item["count"] for item in location_stats},
                "seniority_distribution": {item["_id"]: item["count"] for item in seniority_stats},
                "top_technical_skills": {item["_id"]: item["count"] for item in top_skills},
                "last_updated": datetime.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}

    def search_jobs(self, query: Dict[str, Any], limit: int = 10) -> List[Dict]:
        """
        Search jobs in the MongoDB collection
        
        Args:
            query (Dict[str, Any]): MongoDB query
            limit (int): Maximum number of results
            
        Returns:
            List[Dict]: Search results
        """
        try:
            results = list(self.collection.find(query, {"_id": 0}).limit(limit))
            return results
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            return []

    def close_connection(self):
        """Close MongoDB connection"""
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close()
            logger.info("MongoDB connection closed")