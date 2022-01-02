from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, flash, request
from monologue.auth import bp
from monologue.auth.forms import (
    LoginForm,
    RegistrationForm,
    # ResetPasswordForm,
    # ResetPasswordRequestForm,
)
from monologue.models import User
from monologue.repositories.user import UserRepository
from monologue.utils.decorators import route_not_implemented

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate and request.method == 'POST':
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        login_user(user)
        flash('Login successful', category='message')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_repo = UserRepository()

    if form.validate and request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if user_repo.check_username_is_taken(username):
            flash("Username \"{}\" is taken.".format(username), 'error')
            return render_template('auth/registration.html', form=form)
        elif user_repo.check_email_is_taken(email):
            flash("Email \"{}\" is taken.".format(email), 'error')
            return render_template('auth/registration.html', form=form)

        user = user_repo.create_user(username, email, password)
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('auth/registration.html', form=form)


@bp.route('/reset_password', methods=['GET', 'POST'])
@bp.route('/reset_password/<data>')
@route_not_implemented
def reset_password(data=None):
    pass


@bp.route('/confirm', methods=['GET', 'POST'])
@bp.route('/confirm/<data>', methods=['GET'])
@route_not_implemented
def confirm(data=None):
    pass


@bp.route('/logout')
def logout():
    logout_user()
    flash('Log out successful')
    return redirect(url_for('main.index'))
