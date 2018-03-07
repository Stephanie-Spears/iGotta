import os
import click
import shutil
import subprocess


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
        except:
            print("Error Occured: go back to cli.py and define better exception messages if you want to know why!")

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
        #
        # cmd = 'python ./clean.py'
        # cmd_set = subprocess.call(cmd, shell=True)
        # cmd_check = subprocess.check_output(cmd)
        # cmd_result = cmd_check.decode("utf-8")
        # print("\n\nClean command: ", cmd_result)





    # @app.cli.group()
    # def setapp():
    #     """command group flask setapp registered"""
    #     pass
    #
    # @translate.command()
    # @click.argument('env')
    # def setapp(env):
    #     env_cmd = 'export FLASK_APP=/PycharmProjects/iGotta/' + env
    #     env_set_value = subprocess.call(env_cmd, shell=True)
    #     env_cmd_check = subprocess.check_output(env_cmd)
    #     cmd_result = env_cmd_check.decode("utf-8")
    #     print("\n\nEnv Value: ", cmd_result)

    # # @setapp.command()
    # @setapp.command()
    # @click.argument('env')
    # def setapp(env):
    #     """set export FLASK_APP=env var"""
    #     env_cmd = 'export FLASK_APP=' + env
    #     env_set_value = subprocess.call(env_cmd, shell=True)
    #     env_cmd_check = subprocess.check_output(env_cmd)
    #     if env == 'igotta.py':
    #         debug_cmd = 'export FLASK_DEBUG=0'
    #     if env == 'debug.py':
    #         debug_cmd = 'export FLASK_DEBUG=1'
    #     debug_set_value = subprocess.call(debug_cmd, shell=True)
    #     debug_cmd_check = subprocess.check_output(debug_cmd)
    #     cmd_result = env_cmd_check.decode("utf-8") + debug_cmd_check.decode("utf-8")
    #     print("Env Value: ", env_set_value, "Debug Value:", debug_set_value)

    # @setapp.command()
    # def clean():
    #     remove_files = ["app.db"]
    #     remove_tree = ["migrations/", "logs/", ]
    #
    #     concat_list = remove_files + remove_tree
    #
    #     for item in concat_list:
    #         if not os.path.exists(item):
    #             print("'" + item + "' does not exist.")
    #         if item in remove_files and os.path.exists(item):
    #             os.remove(item)
    #             print("Removed File: " + item)
    #         if item in remove_tree and os.path.exists(item):
    #             shutil.rmtree(item)
    #             print("Removed Tree: " + item)

    # @setapp.command()
    # def newdb():
    #     """instantiate new local db with test data"""
    #
    # @setapp.command()
    # def cleandb():
    #     """wipe database"""
    #
    # @setapp.command()
    # def setdebug():
    #     """set app to FLASK_APP=debug.py + FLASK_DEBUG = 1 (true), and defer to tester db"""
    #
    # @setapp.command()
    # def setflask():
    #     """set app to production db with FLASK_APP=igotta.py + FLASK_DEBUG=0"""
    #
    # @setapp.command()
    # def switchapp():
    #     """switch between modes"""
