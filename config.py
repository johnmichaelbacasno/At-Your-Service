from dotenv import load_dotenv
from os import getenv, path

load_dotenv()

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = getenv('SECRET_KEY')

    MYSQL_DATABASE_HOST = getenv('MYSQL_DATABASE_HOST')
    MYSQL_DATABASE_USER = getenv('MYSQL_DATABASE_USER')
    MYSQL_DATABASE_PASSWORD = getenv('MYSQL_DATABASE_PASSWORD')
    MYSQL_DATABASE_DB = getenv('MYSQL_DATABASE_DB')

    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_BOOTSWATCH_THEME = None

    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'

    UPLOAD_PATH = path.join(path.dirname(__file__), 'flask_uploads')

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass
