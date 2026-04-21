from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Optional

class Settings(BaseSettings):
    # 1. Define variables with types
    # Pydantic will automatically look for these keys in your environment
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432  # Default value if not provided
    DB_NAME: str
    DB_LOGS: str = "False"
    POLL_INTERVAL: int = 60
    
    # Computed property for the full Database URI
    DATABASE_URL: Optional[str] = None

    # 2. Validation logic (Build the connection string automatically)
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: any) -> any:
        if isinstance(v, str):
            return v
        # Accessing validated data from the class attributes
        data = values.data
        return f"postgresql://{data['DB_USER']}:{data['DB_PASSWORD']}@{data['DB_HOST']}:{data['DB_PORT']}/{data['DB_NAME']}"

    # 3. Configuration for .env file loading
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        env_ignore_empty=True
    )

# Instantiate the settings object
settings = Settings()