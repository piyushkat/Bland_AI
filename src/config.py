import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
API_KEY = os.getenv("BLAND_AI_API_KEY")
CALL_URL = "https://api.bland.ai/v1/calls"
TRANSCRIPT_FILE = "transcript.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Country Codes
def load_country_codes():
    try:
        with open("country_codes.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"India": "+91", "USA": "+1", "UK": "+44"}

COUNTRY_CODES = load_country_codes()

# ChromaDB Config
DATA_DIR = "processed_docs"
CHROMA_PERSIST_DIR = os.path.join(DATA_DIR, "chroma_db")