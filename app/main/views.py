from flask import render_template,request,redirect,url_for, abort
from ..models import User, Pitch
from .forms import PitchForm, LoginForm, RegistrationForm, Comment
from . import main
from .. import db
from flask_login import login_required, login_user
from ..email import mail_message

@main.route('/')
# @login_required
def index():
    form = Comment()
    users = User.query.all()
    pitch = [(use, Pitch.query.filter_by(user_id = use.userid).all()) for use in users if len(Pitch.query.filter_by(user_id = use.userid).all())>0]
    user = User.query.filter_by(logged_in = True).first()
    if not user:
        return redirect(url_for('main.login'))
    title = "Welcome to 1MinPitch"
    return render_template('index.html', pitch = pitch, title = title, form = form)

@main.route('/profile')
def profile():
    form = Comment()
    user = User.query.filter_by(logged_in = True).first()
    pitches = Pitch.query.filter_by(user_id = user.userid).all()
    if not user:
        abort(404)
    return render_template('profile.html', user = user, form = form, pitches = pitches)

@main.route('/pitch/new' , methods=['GET','POST'])
# @login_required
def new_pitch():
    user = User.query.filter_by(logged_in = True).first()
    if not user:
        return redirect(url_for('main.login'))
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        date = form.date.data
        new_pitch = Pitch(title = title, category = category, pitch =pitch, date =date, user_id =user.userid)
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
        former_user = User.query.filter_by(logged_in = True).first()
        if former_user:
            former_user.logged_in = False
        db.session.commit()
        current_user = User.query.filter_by(username = form.name.data).first()
        name = form.name.data
        current_user.logged_in = True
        db.session.commit()
        print("ARe they?", current_user.verify_password(form.password.data))
        if current_user is not None and current_user.verify_password(form.password.data):
            print("HERE")
            login_user(current_user)
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
        username = form.username.data
        email = form.email_address.data
        user = User(username = form.username.data,email = form.email_address.data, ipassword = form.password.data, logged_in = False)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to 1MinPitch", "welcome/welcome_user",email,user=user)
        return redirect(url_for('main.login') or url_for('main.login') )
    return render_template('registration.html', reg_form = form, title = title)