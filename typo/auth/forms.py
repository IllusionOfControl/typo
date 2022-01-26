from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Email,
    Length,
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, max=32)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email(), Length(min=9, max=128)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=32)]
    )
    confirm = PasswordField(
        'Confirm', validators=[DataRequired(), EqualTo('password', message="Passwords must match")]
    )


class ResetPasswordRequestForm(FlaskForm):
    def __init__(self):
        raise NotImplementedError


class ResetPasswordForm(FlaskForm):
    def __init__(self):
        raise NotImplementedError