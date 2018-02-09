from datetime import datetime
from iGottaPackage import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
# # from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_imageattach.entity import Image, image_attachment
# from sqlalchemy_imageattach.context import store_context


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_on = db.Column(db.DateTime, default=datetime.utcnow)
    bathrooms = db.relationship('Bathroom', backref='creator', lazy='dynamic')

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# TODO: add rating average, maybe comments
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}, {}, {}>'.format(self.title, self.body, self.user_id)


class Bathroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(360), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # picture = image_attachment('BathroomPicture')
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)

    def set_picture(self, image_filename, image_url):
        if (image_filename and image_url) is not None:
            picture = str(image_filename, image_url)
            return picture
        picture = 'https://s3-us-west-2.amazonaws.com/igotta/resources/poo.png'
        return picture

    def set_infobox(self, title, picture, body):
        infobox = "<div><h1>" + str(title) + "</h1><hr><img src='" + str(picture) + "'><hr><p>" + str(
            body) + "</p></div>"
        return infobox

    # picture = set_picture(image_filename, image_url)

    def __repr__(self):
        return '<Bathroom Lat: {}, Lng: {}, Title: {}, Body: {}, Picture: {}, Infobox: {}, Creator: {}>'.format(self.lat, self.lng, self.title, self.body, self.picture, self.infobox, self.user_id)


#
# class BathroomPicture(db.Model, Image):
#     bathroom_id = db.Column(db.Integer, db.ForeignKey('bathroom.id'), primary_key=True)
#     bathroom = db.relationship('Bathroom')
