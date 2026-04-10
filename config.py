import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    REPOS_DIR = os.path.join(STORAGE_DIR, "repos")
    CHROMA_DIR = os.path.join(STORAGE_DIR, "chroma")
    CACHE_DIR = os.path.join(STORAGE_DIR, "cache")
    
    # Create directories if they do not exist
    os.makedirs(REPOS_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
