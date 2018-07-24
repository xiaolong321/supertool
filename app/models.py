from app.extensions import db, login
from werkzeug import security
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    tools = db.relationship('Tool', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)
    
    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    url = db.Column(db.String(250), index=True, unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))