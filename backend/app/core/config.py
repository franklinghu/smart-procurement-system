"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智能工业品采购系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/procurement"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    # 电商平台API配置
    ZKH_API_URL: str = "https://api.zkh.com/v1"
    ZKH_API_KEY: str = ""
    WEST_API_URL: str = "https://api.west.com/v1"
    WEST_API_KEY: str = ""
    JD_API_URL: str = "https://api.jd.com/v1"
    JD_API_KEY: str = ""
    
    # ERP配置
    YONGYOU_ERP_URL: str = "http://localhost:8080/u8api"
    YONGYOU_ERP_CUSTOMEID: str = ""
    
    # 邮件配置
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()