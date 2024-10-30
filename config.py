import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

class TestingConfig(Config):
    """Testing configuration."""
    FLASK_ENV = 'testing'
    TEST_USER_ID = os.getenv('TEST_USER_ID')
    TEST_USER_NAME = os.getenv('TEST_USER_NAME')
    TEST_CREATION_DATE = os.getenv('TEST_CREATION_DATE')

# A dictionary to help select configuration by name
config = {
    #"development": DevelopmentConfig,
    "testing": TestingConfig
    #"production": ProductionConfig
}