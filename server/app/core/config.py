from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "天机阁占卜平台"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "基于AI的在线占卜平台"
    PROJECT_AUTHOR: str = "仲戌字"
    PROJECT_HOMEPAGE: str = "https://sanshengshui.com"
    
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fortune_platform"
    DATABASE_URI: str = ""
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key"  # 在生产环境中需要修改
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 