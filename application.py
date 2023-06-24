from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from helpers import allowed_file, save_file
from datetime import datetime
import os

from models import db, User, Tweets, Users_Tweets
from forms import RegisterForm, LoginForm
from app import login_manager, app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('main.html', user_logged_in=current_user.is_authenticated)


@app.route('/letters')
def letters():
    tweets = Users_Tweets.query.join(Tweets).order_by(Tweets.date_created.desc()).all()
    return render_template('letters.html', tweets=tweets)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    delete_letter = Tweets.query.filter_by(user_id=current_user.id).order_by(Tweets.date_created.desc()).first()
    if delete_letter:
        db.session.delete(delete_letter)
        db.session.commit()
        return redirect(url_for('letters'))
    else:
        return flash("You haven't any letters")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    photo_url = None
    if form.validate_on_submit():
        photo = form.photo.data
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('/home/hayk/Desktop/MyFlaskProject/Projects', filename='photos/' + filename)
        new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            email=form.email.data,
            photo=photo_url
        )
        print(photo_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form, profile_image=photo_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                flash("Your password is incorrect", "error")
        else:
            flash("Your email is incorrect", "error")
    else:
        flash("Your email and password are incorrect", "error")

    return render_template('login.html', form=form)


@app.route('/post_letter', methods=['GET', 'POST'])
@login_required
def post_letter():
    if request.method == 'POST':
        letter_data = request.form['letter']
        new_letter = Tweets(letter=letter_data, date_created=datetime.now())
        db.session.add(new_letter)
        db.session.commit()

        formm = Users_Tweets(user_id=current_user.id, tweet_id=new_letter.id)
        db.session.add(formm)
        db.session.commit()

        return redirect(url_for('letters'))
    return render_template('post_letter.html')


@app.route('/show_tweets', methods=['GET', 'POST'])
@login_required
def show_tweets():
    tweets = Users_Tweets.query.filter_by(user_id=current_user.id).all()
    return render_template('user_letters.html', tweets=tweets, current_user=current_user)


@app.route('/profile')
@login_required
def profile():
    our_user = Users_Tweets.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', our_user=our_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
