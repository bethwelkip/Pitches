from app.models import Pitch,User, Comment
from app import db, create_app
from werkzeug.security import generate_password_hash, check_password_hash
import os
import unittest

class PitchTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_Bethwel = User(username = 'Bethwel', email = 'kipla@kip.com', logged_in = False, ipassword = generate_password_hash('kip'))
        self.new_pitch = Pitch(pitch="Hi Homey", title = "Hi", category = "Fun" , date= '2020-10-19', downvotes = 7 , upvotes = 0)
        self.new_comment = Comment(comment = "Welcome to tests.")
        db.session.add(self.user_Bethwel)
        db.session.add(self.new_pitch)
        db.session.add(self.new_comment)
        db.session.commit()
        self.assertTrue(len(Pitch.query.all())> 0)
    def tearDown(self):
        Comment.query.delete()
        Pitch.query.delete()
    def test___repr__(self):
        self.assertEqual(self.user_Bethwel.__repr__(), "Bethwel")

if __name__ == '__main__':
    unittest.main()