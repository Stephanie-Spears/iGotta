from flask import render_template, flash, redirect, url_for
from iGottaPackage import app
from iGottaPackage.forms import LoginForm
from flask_login import current_user, login_user
from iGottaPackage.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Stephanie'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

# render_template is a function that comes with the Flask framework. This function takes a template filename and a variable list of template arguments and returns the same template, but with all the placeholders in it replaced with actual values. This also invokes the Jinja2 template engine that comes bundled with the Flask framework.
# A python decorator (@) modifies the function that follows it. Usually they're used to register functions as callbacks for certain events. In this case, the @app.route decorator creates an association between the URL given as an argument and the function. In this example there are two decorators, which associate the URLs '/' and '/index' to this function. This means that when a web browser requests either of these two URLs, Flask is going to invoke this function and pass the return value of it back to the browser as a response.


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
