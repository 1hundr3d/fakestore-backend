import os
import logging
logger = logging.getLogger(__name__)

class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        
        self.SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fakestore.db")
        self.REDIS_URL = os.getenv("REDIS_URL")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    def display_config(self):
        logger.info(f"Конфигурация приложения:")
        logger.info(f"  DATABASE_URL: {self.DATABASE_URL}")
        logger.info(f"  REDIS_URL: {self.REDIS_URL}")
        logger.info(f"  ENVIRONMENT: {self.ENVIRONMENT}")
    