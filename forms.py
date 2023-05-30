from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import InputRequired, Length



class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired('Your username required!'), Length(max=30,
                                                                                                     message='You can not input username that will be more than 30 characters')])
    password = PasswordField('Password:', validators=[InputRequired('Your password required!'),
                                                      Length(max=15, message='Can not be more than 15 characters')])
    email = StringField('Email', validators=[InputRequired('Your email required!')])
    photo = FileField('Photo')


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[InputRequired('Your email required!')])
    password = PasswordField('Password: ', validators=[InputRequired('Your password required!')])


class TweetForm(FlaskForm):
    letter = TextAreaField('Letter')