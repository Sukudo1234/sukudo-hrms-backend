from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres@localhost:5432/postgres"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

