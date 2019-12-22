from app.auth import bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    # ResetPasswordForm,
    # ResetPasswordRequestForm,
)
from app.models import User 
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, flash, request


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate and request.method == 'POST':
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate and request.method == 'POST':
        User.create(username=form.username.data,
                    email=form.email.data,
                    password=form.email.data)
        flash('Your account has been created. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@bp.route('/reset_password', methods=['GET', 'POST'])
@bp.route('/reset_password/<data>')
def reset_password(data=None):
    raise NotImplementedError


@bp.route('/confirm', methods=['GET', 'POST'])
@bp.route('/confirm/<data>', methods=['GET'])
def confirm(data=None):
    raise NotImplementedError


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
