from flask import render_template
from iGottaPackage import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Stephanie'}
    return render_template('index.html', title='Home', user=user)
