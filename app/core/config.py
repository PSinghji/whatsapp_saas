from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "WhatsApp SaaS Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "whatsapp_saas"

    REDIS_URL: str = "redis://localhost:6379/0"

    # Updated for Pydantic V2 compatibility
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        case_sensitive=True
    )

settings = Settings()