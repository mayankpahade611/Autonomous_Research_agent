import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    POSRGRES_URL = os.getenv("POSRGRES_URL")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

settings = Settings()