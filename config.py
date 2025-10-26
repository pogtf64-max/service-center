"""
Конфигурация приложения
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///service_center.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки приложения
    APP_NAME = 'Сервисный центр'
    APP_VERSION = '1.0.0'
    
    # Настройки безопасности
    PASSWORD_MIN_LENGTH = 6
    
    # Настройки пагинации
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Конфигурация для тестов"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

