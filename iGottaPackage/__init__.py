import logging
import os
import re
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch
from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

from config import ProductionConfig, DevelopmentConfig, TestingConfig


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
googlemaps = GoogleMaps()
images = UploadSet('images', IMAGES)


def create_development_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    googlemaps.init_app(app)
    configure_uploads(app, images)

    from iGottaPackage.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from iGottaPackage.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from iGottaPackage.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],
                    app.config['MAIL_PASSWORD'])
            secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='iGotta Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    return app


def create_production_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    googlemaps.init_app(app)
    configure_uploads(app, images)

    from iGottaPackage.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from iGottaPackage.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from iGottaPackage.main import bp as main_bp
    app.register_blueprint(main_bp)

    bonsai = os.environ['BONSAI_URL']
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')
    es_header = [{
        'host': host,
        'port': 443,
        'use_ssl': True,
        'http_auth': (auth[0], auth[1])
    }]
    app.elasticsearch = Elasticsearch(es_header)

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],
                    app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='iGotta Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/igottaProduction.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('iGotta Production Instance Startup')

    return app


def create_testing_app(config_class=TestingConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.testing = True
    app.elasticsearch = None

    from iGottaPackage.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from iGottaPackage.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from iGottaPackage.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from iGottaPackage import models