# services/users/project/config.py


import os



class BaseConfig:
    """Configuración base"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_secretkey"  # nuevo


class DevelopmentConfig(BaseConfig):
    """Configuración de desarrollo"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Configuración de prueba"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Configuración de producción"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
