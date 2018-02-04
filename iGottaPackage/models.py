from datetime import datetime
from iGottaPackage import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# flask_login extension handles our user login, and requires three properties and one method get implemented to work (is_authenticated/is_active/is_anonymous/get_id()). They are pretty generic, so flask-login provides a simple UserMixin class to do it for us.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a post.author expression that will return the user given a post.

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


# Each time the logged-in user navigates to a new page, Flask-Login retrieves the ID of the user from the session, and then loads that user into memory. Flask-Login doesn't connect to the db, so the extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
# The user loader is registered with Flask-Login with the @login.user_loader decorator. The id that Flask-Login passes to the function as an argument is going to be a string, so databases that use numeric IDs need to convert the string to integer as you see above.


# TODO: add rating average, maybe comments
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(140))
    photo = db.Column(db.String(240), nullable=True)
    address = db.Column(db.String(240), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Passing datetime.utcnow function as a default, so SQLAlchemy will set the field to the value of calling that function (note that I did not include the () after utcnow, so the function itself, and not the result of calling it).
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 'user' is the db table, which Flask-SQLAlchemy automatically sets to the name of the model class converted to lowercase.

    def __repr__(self):
        return '<Post {}, {}, {}>'.format(self.title, self.body, self.address)