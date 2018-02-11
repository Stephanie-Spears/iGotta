from flask import Blueprint

bp = Blueprint('auth', __name__)

from iGottaPackage.auth import routes