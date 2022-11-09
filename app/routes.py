from flask import render_template, flash, redirect, url_for
from . import app
from .forms import LoginForm

user = {"username": "vaisakh"}
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

@app.route("/")
def index():
	return render_template('index.html', user=user, posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'login as {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
