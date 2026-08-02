import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for managing environment variables and settings."""
    
    # API Keys
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    SERPER_API_KEY: Optional[str] = os.getenv("SERPER_API_KEY")
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    
    # Model Configuration
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4-turbo-preview")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Vector Store Configuration
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./vector_store")
    
    # PDF Configuration
    UPLOADS_DIR: str = "./uploads"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = 5
    
    # API Timeouts (seconds)
    API_TIMEOUT: int = 10
    
    # LLM Configuration
    LLM_TEMPERATURE: float = 0.7
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate that all required API keys are present.
        
        Returns:
            Tuple of (is_valid, list_of_missing_keys)
        """
        missing_keys = []
        
        if not cls.OPENROUTER_API_KEY:
            missing_keys.append("OPENROUTER_API_KEY")
        
        if not cls.SERPER_API_KEY:
            missing_keys.append("SERPER_API_KEY")
        
        if not cls.OPENWEATHER_API_KEY:
            missing_keys.append("OPENWEATHER_API_KEY")
        
        is_valid = len(missing_keys) == 0
        return is_valid, missing_keys
    
    @classmethod
    def get_validation_message(cls) -> str:
        """
        Get a formatted validation message for missing configuration.
        
        Returns:
            Validation message string
        """
        is_valid, missing_keys = cls.validate()
        
        if is_valid:
            return "✅ All API keys are configured correctly."
        
        message = "⚠️ Missing required API keys:\n\n"
        for key in missing_keys:
            message += f"- {key}\n"
        
        message += "\nPlease add these keys to your .env file."
        return message
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        os.makedirs(cls.UPLOADS_DIR, exist_ok=True)
        os.makedirs(cls.VECTOR_STORE_PATH, exist_ok=True)


# Validate configuration on import
config_valid, missing_keys = Config.validate()
if not config_valid:
    print(f"\n⚠️ Warning: Missing API keys: {', '.join(missing_keys)}")
    print("Please configure these keys in your .env file.\n")

# Setup directories
Config.setup_directories()
