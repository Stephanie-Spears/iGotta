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

    @clean.command()
    @click.argument('filelist', nargs=-1)
    def removefiles(filelist):
        basedir = os.path.abspath(os.path.dirname(__file__))

        remove_files = []
        try:
            for file in filelist:
                # TODO: CHECK IF SETTING BASEDIR GUARD WORKS
                if not str(file).startswith(basedir):
                    print("Base Directory Outside of Project, be careful dummy!")
                    raise Exception
                remove_files.append(str(file.strip()))
                if not os.path.exists(file):
                    print("'" + file + "' does not exist.")
                if file in remove_files and os.path.exists(file):
                    os.remove(file)
                    print("Removed File: " + file)
        except Exception as e:
            print(str(e))

    @click.argument('apptype')
    @clean.command()
    def makeclean(apptype):
        """clear dev env of elasticsearch 'Post' and '.Kibana' indices and database files"""
        remove_db = []
        remove_tree = []
        if apptype == "development":
            print("Removing Elasticsearch Index 'post'\n")
            os.system("curl -XDELETE 'localhost:9200/post?pretty'")
            remove_db.append("app.db")
            remove_tree = ["DevelopmentInstance/migrations/"]

        if apptype == "production":
            print("Removing Bonsai Index 'post'\n")
            os.system("curl -XDELETE '" + str(app.config['BONSAI_URL']) + "/post?pretty'")
            os.system("heroku pg:reset " + "postgresql-silhouetted-21445 --confirm i-gotta")
            remove_tree = ["migrations/", "logs/", "tmp/"]
            os.system("curl -XPUT 'https://qf3n32mxmh:uc4ys1788y@privet-7530964.us-east-1.bonsaisearch.net/post?pretty'")

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

        except Exception as e:
            print("Error Occured: go back to cli.py and define better exception messages if you want to know why!\nJust kidding, here you go:\n" + str(e))

