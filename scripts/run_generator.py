import sys
import os
from dotenv import load_dotenv
from src.utils.api_client import OpenAIClient
from src.generator.jd_generator import JobDescriptionGenerator
from src.utils.file_handler import FileHandler
from src.config import OPENAI_API_KEY

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Generate 200 job descriptions and save to JSON."""
    # Load environment variables from .env file

    if not OPENAI_API_KEY:
        print("⚠️ Please set the OPENAI_API_KEY environment variable in .env file")
        return
    
    api_client = OpenAIClient(OPENAI_API_KEY)
    jd_generator = JobDescriptionGenerator(api_client)
    file_handler = FileHandler()
    
    print("Generating 200 job descriptions...")
    job_descriptions = jd_generator.generate_all_job_descriptions(200)
    
    file_handler.save_to_json(job_descriptions, "data/job_descriptions_dataset.json")
    
    summary = file_handler.generate_summary_report(job_descriptions)
    file_handler.save_to_json(summary, "data/generation_summary.json")

    print("\n" + "="*50)
    print("GENERATION SUMMARY")
    print("="*50)
    print(f"Total Job Descriptions Generated: {summary['total_jobs']}")
    print("\nBy Category:")
    for category, count in summary['categories'].items():
        print(f"  {category}: {count}")
    print(f"\nFiles generated:")
    print(f"  - data/job_descriptions_dataset.json (main dataset)")
    print(f"  - data/generation_summary.json (summary statistics)")

if __name__ == "__main__":
    main()