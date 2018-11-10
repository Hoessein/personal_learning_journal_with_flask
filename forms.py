from wtforms import TextAreaField, DateField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date: DD-MM-YYYY', validators=[DataRequired()], format='%d-%m-%Y')
    time_spent = StringField('Time', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('Resources To Remember', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])



