import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP') or os.path.join(basedir, 'igotta.py')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # todo: switch to production DB when deploying
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD_ONE_ONE')
    ADMINS = [os.environ.get('GMAIL_USERNAME_ONE_ONE')]

    LANGUAGES = ['en', 'es', 'fr', 'ja', 'ru']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    POSTS_PER_PAGE = 10

