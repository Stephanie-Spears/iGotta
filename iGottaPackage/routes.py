from flask import render_template, redirect, url_for, flash, request
from iGottaPackage import app, db, images
from iGottaPackage.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from iGottaPackage.models import User, Post, Bathroom
from werkzeug.urls import url_parse
from iGottaPackage.forms import RegistrationForm, AddBathroomForm
from datetime import datetime
from flask_googlemaps import GoogleMaps, Map
from werkzeug.utils import secure_filename

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),                               'favicon.ico', mimetype='image/png')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_on = datetime.utcnow()
        db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered with iGotta!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    bathrooms = Bathroom.query.all()
    return render_template('index.html', title='Home', bathrooms=bathrooms)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    bathrooms = Bathroom.query.all()
    return render_template('user.html', user=user, bathrooms=bathrooms)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# set up lat/lng parser from addresses? make db pass them in loop here?
@app.route('/maps')
def maps():
    bathrooms = Bathroom.query.all()
    mymap = Map(
        identifier='bathroomMap',
        lat=45.502556,
        lng=-122.632595,
        style="height:100%; width:100%;",
        # maptype_control=True,
        markers=[{'lat': b.lat, 'lng': b.lng, 'infobox': b.set_infobox(b.title, b.image_url, b.body), 'icon': 'static/img/toilet-icon.png'} for b in bathrooms])
    return render_template('maps.html', mymap=mymap,)

    # 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            # {'lat': 45.502556, 'lng': 122.632595, 'infobox': 'test infobox', 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'},
            #      {'lat': 45.502556, 'lng': 122.632595, 'infobox': 'test infobox', 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'}])


@app.route('/add_bathroom', methods=['GET', 'POST'])
@login_required
def add_bathroom():
    form = AddBathroomForm()
    if request.method == 'GET':
        return render_template('add_bathroom.html', form=form)
    if form.validate_on_submit():
        filename = images.save(request.files['bathroom_picture'])
        url = images.url(filename)
        bathroom = Bathroom(title=form.title.data, body=form.body.data, lat=form.lat.data, lng=form.lng.data, image_filename=filename, image_url=url, creator=current_user)
        # bathroom = Bathroom(title=form.title.data, body=form.body.data, lat=form.lat.data, lng=form.lng.data, picture=form.bathroom_picture.data, creator=current_user)
        db.session.add(bathroom)
        db.session.commit()
        flash('Your bathroom has been added!')
        return redirect(url_for('maps'))