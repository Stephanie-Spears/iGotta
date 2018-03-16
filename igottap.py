from iGottaPackage import create_Production_app, db, cli
from iGottaPackage.models import User, Post

#TODO: need to move migration, etc files to allow for concurrent app instances to run (test/dev/prod)
app = create_Production_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}