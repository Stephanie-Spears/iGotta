import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP') or os.path.join(basedir, 'igotta.py')
    DEBUG = False
    TESTING = False
    # force an SQLite database to exist purely in memory is to open the database using the special filename ":memory:". DB ceases to exists once connection is lost
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'es', 'fr', 'ja', 'ru']
    SECRET_KEY = os.environ.get('SECRET_KEY')
    POSTS_PER_PAGE = 10


class ProductionConfig(Config):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')
    ADMINS = [os.environ.get('ADMINS')]

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')

    BONSAI_URL = os.environ.get('BONSAI_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')
    ADMINS = [os.environ.get('ADMINS')]


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
    BONSAI_URL = None



