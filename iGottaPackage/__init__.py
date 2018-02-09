from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
# from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
GoogleMaps(app)
bootstrap = Bootstrap(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
# limit uploads to a max of 16mb
patch_request_class(app)



# Filesystem-backed storage implementation with WSGI middleware which serves actual image files.
# fs_store = HttpExposedFileSystemStore('userimages', 'images/')
#path not right?
# fs_store = HttpExposedFileSystemStore('BathroomPicture', 'static/img/')
# app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)


from iGottaPackage import routes, models

