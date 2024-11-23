from pydantic_settings import BaseSettings

class AISettings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"  # 或者 "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    
    class Config:
        env_file = ".env"

ai_settings = AISettings() 