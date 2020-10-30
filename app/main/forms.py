from flask_wtf import FlaskForm
from ..models import User
from .. import db
from wtforms import StringField, DateField, SubmitField, TextAreaField, PasswordField,ValidationError, validators
from wtforms.validators import Required, Optional, Email
from wtforms import RadioField
class PitchForm(FlaskForm):
    title = StringField('Pitch Title', validators = [Required()])
    category = StringField('Pitch Category',description="For example 'Fun', 'Interview', 'Class'", validators = [Required()])
    pitch = TextAreaField('Your Pitch', validators = [Required()])
    date = DateField('Pitch Date', description = "Use the format YYYY-MM-DD", validators = [Optional()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    name = StringField("Username", validators = [Required()])
    password = PasswordField("Password", validators = [Required()])         
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [Required()])
    email_address =StringField("Email Address", validators = [Required(), Email()])
    password = PasswordField("Password", validators = [Required()])
    password_confirm = PasswordField("Confirm Password")

    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first():
            raise ValidationError(f'That username is no longer available, try {username.data}1234')
    def validate_email(self, email_field):
        if User.query.filter_by(email = email_field.data).first():
            raise ValidationError('That email is already registered here')
   
    
    submit = SubmitField('Submit')