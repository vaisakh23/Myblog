import os
import secrets
from PIL import Image
from . import app, mail
from flask import render_template
from flask_mail import Message


def save_profile_pic(picture):
    '''
    type picture: image file png/jpg
    rtype: string of file name
    reduce size of picture and save to 
    /static/profile_pics with a random name
    '''
    # create file name
    random_hex = secrets.token_hex(8)
    _, file_extention = os.path.splitext(picture.filename)
    picture_file_name = random_hex + file_extention
    picture_saving_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)
    # resize and save picture
    reduce_size_to = (125, 125)
    img = Image.open(picture)
    img.thumbnail(reduce_size_to)
    img.save(picture_saving_path)
    
    return picture_file_name


def send_password_reset_email(user):
    '''
    type user : User model object
    send user the password reset mail
    '''
    token = user.get_reset_password_token()
    msg = Message('Reset Your Password', 
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email])
    msg.body = render_template(
        'email/reset_password.txt', user=user, token=token)
    msg.html = render_template(
        'email/reset_password.html', user=user, token=token)
    mail.send(msg)

