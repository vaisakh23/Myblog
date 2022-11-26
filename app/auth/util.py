from flask import render_template, current_app
from flask_mail import Message
from threading import Thread
from .. import mail

def send_mail_thread(app, msg):
    '''
    baground thread sending mail
    '''
    with app.app_context():
        mail.send(msg)

def send_password_reset_email(user):
    '''
    type user : User model object
    send user password reset instructions
    '''
    token = user.get_reset_password_token()
    msg = Message('Reset Your Password', 
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email])
    msg.body = render_template(
        'email/reset_password.txt', user=user, token=token)
    msg.html = render_template(
        'email/reset_password.html', user=user, token=token)
    #new thread 
    Thread(target=send_mail_thread, args=(
        current_app._get_current_object(), msg)).start()

