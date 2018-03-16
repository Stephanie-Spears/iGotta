from datetime import datetime
from hashlib import md5
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from iGottaPackage import db, login
from iGottaPackage.search import add_to_index, remove_from_index, query_index

# from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
# from sqlalchemy_searchable import SearchQueryMixin
# from sqlalchemy_utils.types import TSVectorType
# from sqlalchemy_searchable import make_searchable


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_on = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except Exception as e:
            return str(e)
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


db.event.listen(db.session, 'before_commit', Post.before_commit)
db.event.listen(db.session, 'after_commit', Post.after_commit)


# class Bathroom():
# class ArticleQuery(db.Model, SearchQueryMixin):
#     pass






# DATABASE MODEL:
#
# app = Flask(__name__)
# csrf = CsrfProtect(app)
# csrf.init_app(app)
#
# db = SQLAlchemy(app)
#
# class ArticleQuery(BaseQuery, SearchQueryMixin):
#     pass
#
#
# class latest_movies_scraper(db.Model):
#     query_class = ArticleQuery
#     __tablename__ = 'latest_movies_scraper'
#     id = db.Column(sa.Integer, primary_key=True)
#     name = db.Column(db.Unicode(255))
#     url = db.Column(db.Unicode(255))
#     image_url = db.Column(db.Unicode(255))
#     create = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     search_vector = db.Column(TSVectorType('name'))
# How i'm saving to database:
#
# check_if_exists = latest_movies_scraper.query.filter_by(name=dictionary['title']).first()
#
#                     if check_if_exists:
#                         print check_if_exists.name
#                         print 'skipping this...'
#                         pass
#                     else:
#
#                         insert_to_db = latest_movies_scraper(name=dictionary['title'], url=dictionary['href'], image_url=dictionary['featured_image'])
#                         db.session.add(insert_to_db)
#                         db.session.commit()
# How I am using search capbilitiy functionality:
#
# name = latest_movies_scraper.query.search(u'Black Panther (2018)').limit(5).all()
# Name returns empty array, but it should return me the name list instead



# SQLAlchemy-Searchable doesn't index existing data. This has to be done manually by performing a synchronisation. For the table definition above the code below is sufficient:
#
# from sqlalchemy_searchable import sync_trigger
#
# def sync_fts():
#     sync_trigger(db.engine, 'latest_movies_scraper', 'search_vector', ['name'])
# This code would normally be part of the db management tools (Flask-Script, Click).