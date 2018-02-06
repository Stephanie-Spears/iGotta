from iGottaPackage import app, db
from iGottaPackage.models import User, Post, Bathroom


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Bathroom': Bathroom, }