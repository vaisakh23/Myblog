from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, EmailField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ..models import User


class ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(max=140)])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Please use a different email address.')


class FollowForm(FlaskForm):
    func_name = HiddenField('hidden')
    submit = SubmitField('submit')


class PostForm(FlaskForm):
    body = TextAreaField('Create new post', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post')


