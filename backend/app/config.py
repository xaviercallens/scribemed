"""Application configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Local LLM Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2:latest"  # or mistral:7b-instruct
    use_local_whisper: bool = True
    whisper_model: str = "base"  # tiny, base, small, medium, large
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # Database
    database_url: str = "sqlite:///./medical_scribe.db"
    
    # Application
    debug: bool = True
    api_port: int = 8001
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
