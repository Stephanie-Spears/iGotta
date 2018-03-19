import os
import click
import shutil


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d iGottaPackage/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d iGottaPackage/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d iGottaPackage/translations'):
            raise RuntimeError('compile command failed')

    @app.cli.group()
    def clean():
        pass

    @click.argument('apptype')
    @clean.command()
    def makeclean(apptype):
        """clear and reset environments"""
        remove_db = []
        remove_tree = []

        # TODO: check that these makecleans work for both
        if apptype == "development":
            print("Removing Elasticsearch Index 'post' and 'bathroom'\n")
            os.system("curl -XDELETE 'localhost:9200/post,bathroom?pretty'")
            remove_db.append("app.db")
            remove_tree = ["DevelopmentInstance/migrations/"]

        if apptype == "production":
            print("Removing Bonsai Index 'post' and 'bathroom'\n")
            bonsai = app.config['BONSAI_URL']
            os.system("curl -XDELETE '" + bonsai + "/post,bathroom?pretty'")
            print("Resetting postgreSQL database: \n")
            os.system("heroku pg:reset " + "postgresql-silhouetted-21445 --confirm i-gotta")
            remove_tree = ["migrations/", "logs/", "tmp/"]

        try:
            concat_list = remove_db + remove_tree
            for item in concat_list:
                if not os.path.exists(item):
                    print("'" + item + "' does not exist.")
                if item in remove_db and os.path.exists(item):
                    os.remove(item)
                    print("Removed File: " + item)
                if item in remove_tree and os.path.exists(item):
                    shutil.rmtree(item)
                    print("Removed Tree: " + item)
            if apptype == "development":
                print("Adding Sqlite database back:\n")
                os.system("flask db init -d 'DevelopmentInstance/migrations'")
                os.system("flask db migrate -d 'DevelopmentInstance/migrations/'")
                os.system("flask db upgrade  -d 'DevelopmentInstance/migrations/'")
                print("Adding Elasticsearch index 'post' and 'bathroom': ")
                os.system("curl -XPUT 'localhost:9200/post?pretty'")
                os.system("curl -XPUT 'localhost:9200/bathroom?pretty'")
            if apptype == "production":
                print("Adding PostgreSQL database back: \n")
                os.system("flask db init")
                os.system("flask db migrate")
                os.system("flask db upgrade")
                print("Adding Bonsai Index 'post' and 'bathroom': \n")
                os.system("curl -XPUT " + bonsai + " '/post?pretty'")
                os.system("curl -XPUT " + bonsai + " '/bathroom?pretty'")

        except Exception as e:
            print("Error Occured: go back to cli.py and define better exception messages if you want to know why!\nJust kidding, here you go:\n" + str(e))

