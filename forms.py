from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (
                                DataRequired, Regexp, ValidationError, Email,
                                EqualTo, Length
                                )

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Please use a different email')


class Register(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
           ])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('confirm', message='Passwords must match')

        ])

    confirm = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired()
        ])


class Login(FlaskForm):
    email = StringField(
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        validators=[
            DataRequired()
        ])
