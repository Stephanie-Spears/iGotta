from flask import render_template
from iGottaPackage import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Stephanie'}
    return render_template('index.html', title='Home', user=user)

# To render the template I had to import a function that comes with the Flask framework called render_template(). This function takes a template filename and a variable list of template arguments and returns the same template, but with all the placeholders in it replaced with actual values.


# A python decorator (@) modifies the function that follows it. Usually they're used to register functions as callbacks for certain events. In this case, the @app.route decorator creates an association between the URL given as an argument and the function. In this example there are two decorators, which associate the URLs '/' and '/index' to this function. This means that when a web browser requests either of these two URLs, Flask is going to invoke this function and pass the return value of it back to the browser as a response.
