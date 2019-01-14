from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import (
                                DataRequired, ValidationError, Email,
                                EqualTo, Length, InputRequired
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


class TacoOrder(FlaskForm):
    protein = StringField(
        'Choose Protein',
        validators=[
            DataRequired()

        ])
    shell = StringField(
        'Choose Your Shell',
        validators=[
            DataRequired()
        ]
    )
    cheese = BooleanField(
        'Would you like cheese'
    )
    extras = TextAreaField(
        validators=[
            InputRequired()
        ]
    )
