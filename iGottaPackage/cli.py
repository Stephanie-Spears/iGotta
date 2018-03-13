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
    @click.argument('dblist', nargs=-1)
    def makeclean(dblist):
        remove_files = []
        try:
            for db in dblist:
                remove_files.append(str(db.strip()))
                print("Remove Files: ", remove_files)
                if not db.endswith(".db"):
                    raise ValueError("Error: database files must have the '.db' file extension to be removed.")
        except Exception as e:
            print("Error Occured: go back to cli.py and define better exception messages if you want to know why!\nJust kidding, here you go:\n" + str(e))

        remove_tree = ["migrations/", "logs/", "tmp/"]

        concat_list = remove_files + remove_tree

        for item in concat_list:
            if not os.path.exists(item):
                print("'" + item + "' does not exist.")
            if item in remove_files and os.path.exists(item):
                os.remove(item)
                print("Removed File: " + item)
            if item in remove_tree and os.path.exists(item):
                shutil.rmtree(item)
                print("Removed Tree: " + item)