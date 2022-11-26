import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    moment = Moment(app)
    
    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    if not app.debug:
        #logging to file
        file_handler = RotatingFileHandler(
            'myblog.log', maxBytes=10240,
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
                app.config['MAIL_SERVER'], 
                app.config['MAIL_PORT']
            ),
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=app.config['ADMINS'],
            subject='Myblog Failure',
            credentials=(
                app.config['MAIL_USERNAME'],
                app.config['MAIL_PASSWORD']
            ),
            secure=()
            )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        app.logger.error("testing logging")
    
    return app
    
    
from . import models
