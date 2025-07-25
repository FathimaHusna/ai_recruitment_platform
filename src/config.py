import os

from dotenv import load_dotenv
load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://nusrathamtha:${MONGO_PASSWORD}@cluster0.rosecne.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "recruitment_platform")
INPUT_FILE = os.getenv("INPUT_FILE", "data/job_descriptions_dataset.json")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")