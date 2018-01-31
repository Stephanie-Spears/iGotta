from flask import Flask
from config import Config

#  In Python, a sub-directory that includes a __init__.py file is considered a package, and can be imported. When you import a package, the __init__.py executes and defines what symbols the package exposes to the outside world.


app = Flask(__name__)
app.config.from_object(Config)


from iGottaPackage import routes
# The script above simply creates the application object as an instance of class Flask imported from the flask package. The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used. Flask uses the location of the module passed here as a starting point when it needs to load associated resources such as template files. The application then imports the routes module.
# The routes module is imported at the bottom and not at the top of the script as it is always done. The bottom import is a workaround to circular imports, a common problem with Flask applications.