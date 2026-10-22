from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./requisitions.db"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    llm_api_key: str = ""
    po_api_url: str = "http://127.0.0.1:8080"
    
    class Config:
        env_file = ".env"


settings = Settings()
