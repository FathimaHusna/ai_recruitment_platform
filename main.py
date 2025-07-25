# main.py
import os
from dotenv import load_dotenv
from api_client import OpenAIClient
from jd_generator import JobDescriptionGenerator
from file_handler import FileHandler

def main():
    """Generate 200 job descriptions and save to JSON."""
    # Load environment variables from .env file
    load_dotenv()

    API_KEY = os.getenv("OpenAI_API_Key")
    if not API_KEY:
        print("⚠️ Please set the OpenAI_API_Key environment variable in .env file")
        return
    
    api_client = OpenAIClient(API_KEY)
    jd_generator = JobDescriptionGenerator(api_client)
    file_handler = FileHandler()
    
    print("Generating 200 job descriptions...")
    job_descriptions = jd_generator.generate_all_job_descriptions(200)
    
    file_handler.save_to_json(job_descriptions, "job_descriptions_dataset.json")
    
    summary = file_handler.generate_summary_report(job_descriptions)
    file_handler.save_to_json(summary, "generation_summary.json")
    
    print("\n" + "="*50)
    print("GENERATION SUMMARY")
    print("="*50)
    print(f"Total Job Descriptions Generated: {summary['total_jobs']}")
    print("\nBy Category:")
    for category, count in summary['categories'].items():
        print(f"  {category}: {count}")
    print(f"\nFiles generated:")
    print(f"  - job_descriptions_dataset.json (main dataset)")
    print(f"  - generation_summary.json (summary statistics)")

if __name__ == "__main__":
    main()