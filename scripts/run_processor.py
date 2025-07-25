import json
import logging
from src.processor.processor import JobDescriptionProcessor
from src.config import OPENAI_API_KEY, MONGO_URI, DATABASE_NAME, INPUT_FILE

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to run the job description processor
    """
    if not OPENAI_API_KEY:
        logger.error("⚠️ Please set OPENAI_API_KEY in .env")
        return
    
    if not MONGO_URI or "${MONGO_PASSWORD}" in MONGO_URI:
        logger.error("⚠️ Please set MONGO_URI with a valid password in .env")
        return
    
    try:
        processor = JobDescriptionProcessor(
            openai_api_key=OPENAI_API_KEY,
            mongo_uri=MONGO_URI,
            database_name=DATABASE_NAME
        )
        
        print("Starting job description processing...")
        summary = processor.process_all_job_descriptions("data/job_descriptions_dataset.json")
        
        with open("data/processing_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        stats = processor.get_collection_stats()
        with open("data/collection_stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Jobs: {summary['total_jobs']}")
        print(f"Successfully Processed: {summary['successful_processed']}")
        print(f"Successfully Stored: {summary['successful_stored']}")
        print(f"Failed Processing: {summary['failed_processed']}")
        print(f"Failed Storage: {summary['failed_stored']}")
        
        print("\n" + "="*60)
        print("COLLECTION STATISTICS")
        print("="*60)
        print(f"Total Jobs in Database: {stats['total_jobs']}")
        print("\nTop Categories:")
        for category, count in list(stats['category_distribution'].items())[:5]:
            print(f"  {category}: {count}")
        
        print("\nTop Technical Skills:")
        for skill, count in list(stats['top_technical_skills'].items())[:10]:
            print(f"  {skill}: {count}")
        
        print(f"\nFiles generated:")
        print(f"  - data/processing_summary.json")
        print(f"  - data/collection_stats.json")

        processor.close_connection()
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()