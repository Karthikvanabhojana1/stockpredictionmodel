"""
Configuration management for Soros Chatbot
Loads settings from environment variables and .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Config:
    """Configuration class for Soros Chatbot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    
    # Server Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
    
    # Development Settings
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # File Paths
    DATA_DIR = Path(__file__).parent / "data"
    KNOWLEDGE_BASE_DIR = DATA_DIR / "soros"
    PDF_DIR = DATA_DIR / "pdfs"
    PDF_PROCESSED_DIR = PDF_DIR / "processed"
    PDF_UPLOADS_DIR = PDF_DIR / "uploads"
    PDF_ARCHIVE_DIR = PDF_DIR / "archive"
    
    # PDF Processing Settings
    MAX_PDF_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", "50"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. Please set it in your .env file or environment variables.\n"
                "Create a .env file in the project root with:\n"
                "OPENAI_API_KEY=your-api-key-here"
            )
        
        return True
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [
            cls.DATA_DIR,
            cls.KNOWLEDGE_BASE_DIR,
            cls.PDF_DIR,
            cls.PDF_PROCESSED_DIR,
            cls.PDF_UPLOADS_DIR,
            cls.PDF_ARCHIVE_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without sensitive data)"""
        print("🔧 Soros Chatbot Configuration:")
        print(f"   OpenAI Model: {cls.OPENAI_MODEL}")
        print(f"   Temperature: {cls.OPENAI_TEMPERATURE}")
        print(f"   Max Tokens: {cls.OPENAI_MAX_TOKENS}")
        print(f"   API Host: {cls.API_HOST}")
        print(f"   API Port: {cls.API_PORT}")
        print(f"   Frontend Port: {cls.FRONTEND_PORT}")
        print(f"   Debug Mode: {cls.DEBUG}")
        print(f"   Log Level: {cls.LOG_LEVEL}")
        print(f"   API Key Set: {'✅ Yes' if cls.OPENAI_API_KEY else '❌ No'}")
        print(f"   PDF Directory: {cls.PDF_DIR}")
        print(f"   Max PDF Size: {cls.MAX_PDF_SIZE_MB}MB")
        print(f"   Chunk Size: {cls.CHUNK_SIZE}")
        print(f"   Chunk Overlap: {cls.CHUNK_OVERLAP}")

# Create .env file if it doesn't exist
def create_env_file():
    """Create a .env file with default values if it doesn't exist"""
    env_path = Path(__file__).parent / ".env"
    
    if not env_path.exists():
        env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here

# Optional: Customize API settings
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=3000

# Development Settings
DEBUG=true
LOG_LEVEL=INFO

# PDF Processing Settings
MAX_PDF_SIZE_MB=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
"""
        
        try:
            with open(env_path, 'w') as f:
                f.write(env_content)
            print(f"✅ Created .env file at {env_path}")
            print("📝 Please edit the .env file and set your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    
    return True

if __name__ == "__main__":
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Ensure directories exist
    Config.ensure_directories()
    
    # Print current configuration
    Config.print_config()
    
    # Validate configuration
    try:
        Config.validate()
        print("✅ Configuration is valid")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📝 To fix this:")
        print("1. Create a .env file in the project root")
        print("2. Add your OpenAI API key:")
        print("   OPENAI_API_KEY=your-actual-api-key-here")
        print("3. Get an API key from: https://platform.openai.com/api-keys") 