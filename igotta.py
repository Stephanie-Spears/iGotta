from iGottaPackage import app, db
from iGottaPackage.models import User, Post
# a Python script at the top-level that defines the Flask application instance



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}