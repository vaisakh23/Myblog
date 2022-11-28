from flask import (render_template, flash, 
    redirect, url_for, request)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .. import db
from ..models import User
from . import bp
from .forms import (LoginForm, RegistrationForm,ResetPasswordRequestForm,
    ResetPasswordForm)
from .util import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # successful login
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page  or url_parse(next_page).netloc != '':
                #ensures that the redirect stays within the
                #same site as the application
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            # unsuccessful login
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login')) 
    return render_template('auth/reset_password_request.html', form=form, title='Reset password')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired link')
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, title='Reset password')
        


