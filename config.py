import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f8jqlbmv6tc5utmr'
    FLASK_APP = os.environ.get('FLASK_APP') or 'igotta.py'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY') or '02d36d7fdfa549bcb3884dbe2d5eb87f'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200/'
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or 'AIzaSyBAKH4IaBUcaJdJf6xFWKhfoSKpO5O26rY'
    HEROKU_DATABASE_URL = os.environ.get('HEROKU_DATABASE_URL') or 'postgres://jwuvdtxomudpcg:22dc713d15b9ee4645c2dda59de3c06ec72cf28468319a7b8046d0f88fbbe9e1@ec2-23-23-92-179.compute-1.amazonaws.com:5432/d6cl71kft21b6t'
