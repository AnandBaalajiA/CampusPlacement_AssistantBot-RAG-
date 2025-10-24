"""
Application configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'gemini-embedding-001')
    GENERATION_MODEL = os.getenv('GENERATION_MODEL', 'gemini-2.0-flash-exp')
    EMBEDDING_DIMENSION = int(os.getenv('EMBEDDING_DIMENSION', 768))
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Vector database
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'vector_db/indexes')
    METADATA_PATH = os.getenv('METADATA_PATH', 'vector_db/metadata')
    
    # Chunking
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    
    # Retrieval
    TOP_K_CHUNKS = int(os.getenv('TOP_K_CHUNKS', 5))
    
    # Generation
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.1))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', 500))
