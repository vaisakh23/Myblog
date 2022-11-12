from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from . import app, db
from .forms import LoginForm, RegistrationForm
from .models import User, Post


posts = [
    {
        "author": {"username": "jhon"},
        "body": "Beautiful day it is!"
    },
    {
        "author": {"username": "mike"},
        "body": "rainly day"
    }
    ]

@app.route('/')
@login_required
def index():
	return render_template('index.html', posts=posts)

@app.route('/profile')
@login_required
def profile():
    return 'profile page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
                next_page = url_for('index')
            return redirect(next_page)
        else:
            # unsuccessful login
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
