import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "50000"))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))

    SUMMARY_LENGTH = int(os.getenv("SUMMARY_LENGTH", "3"))

    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    APP_NAME = "Text Summarization with RAG"
    APP_VERSION = "1.0.0"

settings = Settings()
