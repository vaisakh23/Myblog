from time import time
import jwt
from . import db, login_manager, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    
#associate table for many-many relation
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    #hashed password for security
    password_hash = db.Column(db.String(128), nullable=False) 
    #one-many relationship with post
    #creates author attribute to Post class
    posts = db.relationship(
        'Post', 
        backref='author', 
        lazy='dynamic'
    )
    profile_pic_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #many-many relation, self referential
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f"{self.username}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        #compare input password to User's hashed password
        return check_password_hash(self.password_hash, password)
    
    def follow(self, user):
        if not self.is_in_followed(user):
            #followed user
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_in_followed(user):
            #unfollow user
            self.followed.remove(user)
        
    def is_in_followed(self, user):
        #return true if user exist in followed relation list, false otherwise
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def followed_users_posts(self):
        #all the post from followed users
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        #own posts
        own = Post.query.filter_by(user_id=self.id)
        #combine and order
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def get_reset_password_token(self, expires_in=600):
        '''
        return JWT token as a string
        '''
        return jwt.encode(
            {'user_id': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
        
    @staticmethod
    def verify_reset_password_token(token):
        '''
        return User object if valid token else None
        '''
        try:
            user_id = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), )
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
