from iGottaPackage import create_Development_app, db, cli
from iGottaPackage.models import User, Post

app = create_Development_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}