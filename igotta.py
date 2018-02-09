from iGottaPackage import app, db, cli
from iGottaPackage.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}