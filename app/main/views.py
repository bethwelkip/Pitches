from flask import render_template,request,redirect,url_for, abort
from ..models import User, Pitch, Comment
from .forms import PitchForm, LoginForm, RegistrationForm, Upvote, Downvote
from .forms import  Comment as CommentForm
from . import main
from .. import db
from flask_login import login_required, login_user, logout_user
from ..email import mail_message
from werkzeug.security import generate_password_hash,check_password_hash

def save_users():
    users = User.query.all()

    print(type(users[0]))

    comments = Comment.query.all()
    print(comments)
    pitches = Pitch.query.all()
    print(pitches)

@main.route('/logout')
def logout():
    former_user = User.query.filter_by(logged_in = True).first()
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/')
# @login_required
def index():
    # save_users()
    form = CommentForm()
    users = User.query.all()
    pitch = [(use, Pitch.query.filter_by(user_id = use.userid).all()) for use in users if len(Pitch.query.filter_by(user_id = use.userid).all())>0]
    user = User.query.filter_by(logged_in = True).first()
    if not user:
        return redirect(url_for('main.login'))
    title = "Welcome to 1MinPitch"
    return render_template('index.html', pitch = pitch, title = title, form = form)

@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    user = User.query.filter_by(logged_in = True).first()
    print(user.username)
    pitches = Pitch.query.filter_by(user_id = user.userid).all()
    pit = sorted(pitches, reverse = True, key= lambda x: x.date)
    # for pitch in pit:
    #     print(pitch.date)
    #  for makinf sure it reverses the sort.
    if not user:
        abort(404)
    return render_template('profile.html', user = user, pitches = pit)

@main.route('/pitch/new' , methods=['GET','POST'])
@login_required
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
        new_pitch = Pitch(title = title,upvotes = 0, downvotes = 0, category = category, pitch =pitch, date =date, user_id =user.userid)
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
        if current_user and current_user.verify_password(form.password.data):
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
        user = User(username = form.username.data,email = form.email_address.data, ipassword = generate_password_hash(form.password.data), logged_in = False)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to 1MinPitch", "welcome/welcome_user",email,user=user)
        return redirect(url_for('main.login') or url_for('main.login') )
    return render_template('registration.html', reg_form = form, title = title)

@main.route('/<pitch>/comment/', methods = ['GET', 'POST'])
@login_required
def comment(pitch):
    user = User.query.filter_by(logged_in = True).first()
    if not user:
        return redirect(url_for('main.login'))
    current_pitch = Pitch.query.filter_by(title = pitch).first()
    form = CommentForm()
    upvote = Upvote()
    if upvote.upvote.data:
        current_pitch.upvotes = current_pitch.upvotes + 1
        db.session.commit()
        return redirect(url_for('main.comment', pitch = current_pitch.title))
    downvote = Downvote()
    if downvote.downvote.data:
        current_pitch.downvotes = current_pitch.downvotes + 1
        db.session.commit()
        print(current_pitch.downvotes)
        return redirect(url_for('main.comment', pitch = current_pitch.title))
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(comment = comment, pitch_id = current_pitch.pitch_id )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.comment', pitch = current_pitch.title))
    comments = Comment.query.filter_by(pitch_id = current_pitch.pitch_id).all()
    print(current_pitch.date.date())
    return render_template("comment.html", date = [current_pitch.date.date(), current_pitch.date.time()], votes = [current_pitch.upvotes, current_pitch.downvotes], downvote = downvote, upvote = upvote, pitch = current_pitch, form = form, comments = comments, user = user.username)
