import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    """Parents configuration class."""
    DEBUG = False
    CSRF_ENABLE = True
    SECRET = os.getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    print(SQLALCHEMY_DATABASE_URI)

class DevelopmentConfig(Config):
    """ Configurations for Development"""
    #DEBUG = True

class TestingConfig(Config):
    """ Configurations for Development"""

class ProductionConfig(Config):
    """ Configurations for Development"""

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}