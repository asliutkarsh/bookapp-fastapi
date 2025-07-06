
from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URL: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    @cached_property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_URL}/{self.POSTGRES_DB}"

    
Config = Settings()