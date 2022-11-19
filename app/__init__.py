import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if not app.debug:
    #logging to file
    file_handler = RotatingFileHandler(
        'microblog.log', maxBytes=10240,
        backupCount=10
        )
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    
    #app.logger.info("testing logging")
    
    #logging to mail
    mail_handler = SMTPHandler(
        mailhost=(
            os.environ.get('MAIL_SERVER'), 
            os.environ.get('MAIL_PORT')
        ),
        fromaddr=os.environ.get('MAIL_USERNAME'),
        toaddrs=os.environ.get('ADMIN'),
        subject='Microblog Failure',
        credentials=(
            os.environ.get('MAIL_USERNAME'),
            os.environ.get('MAIL_PASSWORD')
        ),
        secure=()
        )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    #app.logger.error("testing logging")

from . import routes, models, errors
