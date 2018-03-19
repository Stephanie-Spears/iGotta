from iGottaPackage import create_production_app, db, cli
from iGottaPackage.models import User, Post

app = create_production_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}