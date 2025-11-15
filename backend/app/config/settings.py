from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
 