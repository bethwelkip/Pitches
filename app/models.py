from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(255))
    ipassword = db.Column(db.String(255))
    email = db.Column(db.String(255)) 
    logged_in = db.Column(db.Boolean)
    pitches = db.relationship('Pitch',backref = 'user',lazy="dynamic")
    

    def __repr__(self):
        return f'{self.username}'
    def get_id(self):
           return (self.userid)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password_hash(self, password):
        self.ipassword = generate_password_hash(password)
    
    def verify_password(self, password):
        # print("########", self._password, "|||||||",passw, "#######")
        return check_password_hash(self.ipassword,password)


class Pitch(UserMixin, db.Model):
    __tablename__ = 'pitches'
    pitch_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    pitch = db.Column(db.String())
    date = db.Column(db.DateTime())
    downvotes = db.Column(db.Integer)
    upvotes = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.userid'))
    pitches = db.relationship('Comment',backref = 'pitch',lazy="dynamic")
    def __repr__(self):
        return f'{self.title}'

class Comment(UserMixin, db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String())
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.pitch_id'))
    def __repr__(self):
        return f'{self.comment}'
