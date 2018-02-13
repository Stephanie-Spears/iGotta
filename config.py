import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP') or os.path.join(basedir, 'igotta.py')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # todo: switch to production (env var AND filename -> production-app.db)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'production_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')
    ADMINS = [os.environ.get('ADMINS')]

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    LANGUAGES = ['en', 'es', 'fr', 'ja', 'ru']

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')

    POSTS_PER_PAGE = 10

    #
    #
    # BONSAI_URL = os.environ.get('BONSAI_URL')
    # BONSAI_ACCESS_SECRET = os.environ.get('BONSAI_ACCESS_SECRET')
    # BONSAI_ACCESS_KEY = os.environ.get('BONSAI_ACCESS_KEY')