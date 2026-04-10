from groq import Groq
from config import Config

def get_groq_client():
    """Initializes and returns the Groq client instance."""
    return Groq(api_key=Config.GROQ_API_KEY)
