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
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')

    #file uploading
    UPLOADS_DEFAULT_DEST = basedir + str(os.environ.get('UPLOADS_DEFAULT_DEST'))
    UPLOADS_DEFAULT_URL = os.environ.get('UPLOADS_DEFAULT_URL')
    UPLOADED_IMAGES_DEST = basedir + str(os.environ.get('UPLOADS_IMAGES_DEST'))
    UPLOADED_IMAGES_URL = os.environ.get('UPLOADED_IMAGES_URL')

    #file storage
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')