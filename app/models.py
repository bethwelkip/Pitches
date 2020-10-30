from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(255))
    password = db.Column(db.String())
    email = db.Column(db.String()) 
    def __repr__(self):
        return f'{self.username}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @classmethod
    def password_hash(self, password):
        self.password = generate_password_hash(password)
        return password
    
    def verify_password(self, passw):
        return check_password_hash(self.password,passw)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

class Pitch(UserMixin, db.Model):
    __tablename__ = 'pitches'
    pitch_id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    pitch = db.Column(db.String())
    date = db.Column(db.DateTime())
    def __repr__(self):
        return f'{self.username}'
