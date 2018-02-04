from datetime import datetime
from iGottaPackage import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a post.author expression that will return the user given a post.

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.email)


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