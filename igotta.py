from iGottaPackage import create_Development_app, create_Production_app, db, cli
from iGottaPackage.models import User, Post

# TODO: change to production when deploying
# app = create_Production_app()
app = create_Development_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}