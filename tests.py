#!/usr/bin/env python
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py', 'venv/*'])
cov.start()

import os
import unittest
from datetime import datetime, timedelta
from config import TestingConfig, basedir
from iGottaPackage import create_testing_app, db
from iGottaPackage.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_testing_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='John', email='John@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='John', email='John@example.com')
        u2 = User(username='Susan', email='Susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'John')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='John', email='John@example.com')
        u2 = User(username='Susan', email='Susan@example.com')
        u3 = User(username='Mary', email='Mary@example.com')
        u4 = User(username='David', email='David@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from John", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from Susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from Mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from David", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # John follows Susan
        u1.follow(u4)  # John follows David
        u2.follow(u3)  # Susan follows Mary
        u3.follow(u4)  # Mary follows David
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

    def test_delete_post(self):
        # create a user and a post
        u = User(username='John', email='John@example.com')
        p = Post(body='test post', author=u, timestamp=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        # query the post and destroy the session
        p = Post.query.get(1)
        db.session.remove()
        # delete the post using a new session
        db.session = db.create_scoped_session()
        db.session.delete(p)
        db.session.commit()


    # Doesn't give more coverage percentage during debug. Necessary test?
    def test_validate_username(self):
        def validate_username(username):
            if User.query.filter_by(username=username).first() is None:
                return username
            version = 2
            while True:
                new_username = username + str(version)
                if User.query.filter_by(username=new_username).first() is None:
                    break
                version += 1
            return new_username
        # create a user and write it to the database
        u = User(username='John', email='John@example.com')
        # u = User(username='John', email='John@example.com')
        db.session.add(u)
        db.session.commit()
        username = validate_username('Susan')
        assert username == 'Susan'
        username = validate_username('John')
        assert username != 'John'
        # make another user with the new username
        u = User(username=username, email='Susan@example.com')
        db.session.add(u)
        db.session.commit()
        username2 = validate_username('John')
        assert username2 != 'John'
        assert username2 != username


if __name__ == '__main__':
    try:
        unittest.main(verbosity=2)
    except Exception as e:
        print(str(e))
        pass
    except BaseException as e:
        print(str(e))
        pass
    cov.stop()
    cov.save()
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()