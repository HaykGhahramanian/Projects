from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, TweetForm
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



app = Flask(__name__)


app.config['SECRET_KEY'] = 'MYSECRETKEY!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/User/PycharmProjects/pythonProject2/Flask_Project/wot.db'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(15))
    email = db.Column(db.String(30))
    photo = db.Column(db.String(350))

    letters = db.relationship('Tweets', backref='user', lazy='dynamic')


class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    letter = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('main.html', user_logged_in=current_user.is_authenticated)


@app.route('/letters')
def letters():
    letters = Tweets.query.all()
    return render_template('letters.html', letters=letters)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    a = True
    if a:
        delete_letter = Tweets.query.filter_by(user_id=current_user.id).order_by(Tweets.date_created.desc()).first()
        if delete_letter:
            db.session.delete(delete_letter)
            db.session.commit()
            return redirect(url_for('letters'))

    return render_template('index.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data),
                        email=form.email.data,
                        photo=form.photo.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


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
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/post_letter', methods=['GET', 'POST'])
@login_required
def post_letter():
    form = TweetForm()

    if form.validate_on_submit():
        new_letter = Tweets(user_id=current_user.id, letter=form.letter.data, date_created=datetime.now())
        db.session.add(new_letter)
        db.session.commit()

        return redirect(url_for('letters'))
    return render_template('post_letter.html', form=form)


@app.route('/show_tweets', methods=['GET', 'POST'])
@login_required
def show_tweets():
    user = Tweets.query.filter_by(user_id=current_user.id).all()
    return render_template('user_letters.html', user=user, current_user=current_user)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
