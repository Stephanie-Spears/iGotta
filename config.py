import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP') or os.path.join(basedir, 'igotta.py')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretdontstealitplzlolololz'

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
