from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User

from flask_wtf import Form
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


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    date = DateField('date', validators=[DataRequired()])
    time_spent = StringField('time', validators=[DataRequired()])
    what_i_learned = TextAreaField('learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('resources', validators=[DataRequired()])
    submit = SubmitField('Submit')

