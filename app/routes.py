from flask import (render_template, flash, 
    redirect, url_for, request, abort)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from . import app, db
from .forms import LoginForm, RegistrationForm, ProfileEditForm, FollowForm
from .models import User, Post
from .util import save_profile_pic

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


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@login_required
def index():
    return render_template('index.html', posts=posts)

#profile
@app.route('/user/<username>')
@login_required
def user(username):
    form = FollowForm()
    user = User.query.filter_by(username=username).first_or_404()
    profile_pic_uri = url_for('static' ,filename='profile_pics/' + user.profile_pic_file)
    return render_template('user.html', user=user, posts=posts, profile_pic_uri=profile_pic_uri, form=form)


@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileEditForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            pic_file_name = save_profile_pic(form.profile_pic.data)
            current_user.profile_pic_file = pic_file_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('user', username=current_user.username))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('profile_edit.html', form=form)

    
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


@app.route('/follow_unfollow/<username>', methods=['POST'])
@login_required
def follow_unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        if current_user == user:
            flash("Something fishy")
            return redirect(url_for('index'))
        #app.logger.info(form.func_name.data)
        if form.func_name.data == 'follow':
            current_user.follow(user)
            flash('Followed successfully')
        elif form.func_name.data == 'unfollow':
            current_user.unfollow(user)
            flash('Unfollowed successfully')
        db.session.commit()
    return redirect(url_for('user', username=username))   


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        current_user.unfollow(user)
        db.session.commit()
        flash('Unfollowed successfully')
    return redirect(url_for('user', username=username))   

