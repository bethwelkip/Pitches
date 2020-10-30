from flask import render_template,request,redirect,url_for
from ..models import User, Pitch
from .forms import PitchForm, LoginForm, RegistrationForm
from . import main
from .. import db
from flask_login import login_required, login_user
from ..email import mail_message

@main.route('/')
@login_required
def index():
    title = "Welcome to 1MinPitch"
    return render_template('index.html', title = title)

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/pitch/new' , methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        date = form.date.data
        new_pitch = Pitch(title = title, category = category, pitch =pitch, date =date)
        db.session.add(new_pitch)
        db.session.commit()
        return redirect(url_for('main.index'))
    title = "Add New Pitch"
    return render_template('pitchform.html', pitch_form = form ,title = title)


@main.route('/login', methods=[ 'GET','POST'])
def login():
    form = LoginForm()
    title = "Please Login into your account"
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        name = form.name.data
        print("ARe they?", user.verify_password(form.password.data))
        if user is not None and user.verify_password(form.password.data):
            print("HERE")
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            print("**************************************")
            redirect(url_for('main.login'))
    return render_template('login.html', login_form = form, title = title)

@main.route('/registration', methods = ['GET', 'POST'])
def registration():
    form = RegistrationForm()
    title = "Welcome  to 1MinPitch!!!"
    if form.validate_on_submit():
        # username = form.username.data
        # email = form.email_address.data
        user = User(username = form.username.data,email = form.email_address.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to 1MinPitch", "welcome/welcome_user",email,user=user)
        return redirect(url_for('main.login') or url_for('main.login') )
    return render_template('registration.html', reg_form = form, title = title)