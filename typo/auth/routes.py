from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, flash, request
from typo.auth import bp
from typo.auth.forms import (
    LoginForm,
    RegistrationForm,
    # ResetPasswordForm,
    # ResetPasswordRequestForm,
)
from typo.repositories import user as user_repo
from typo.utils.decorators import route_not_implemented


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = user_repo.get_user_by_username(username)
        if user:
            from typo.utils.crypto import verify_password

            if verify_password(user.password, password):
                login_user(user)
                flash('Login successful.', category='message')
                return redirect(url_for('main.index')), 200
        flash('Invalid username or password.', category='error')
    return render_template('auth/login.html', form=form), 400


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate and request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if user_repo.check_username_is_taken(username):
            flash("Username \"{}\" is taken.".format(username), 'error')
            return render_template('auth/registration.html', form=form), 400

        if user_repo.check_email_is_taken(email):
            flash("Email \"{}\" is taken.".format(email), 'error')
            return render_template('auth/registration.html', form=form), 400

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
