from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.Integer, db.ForeignKey('location.id'))
    health = db.Column(db.Integer)
    max_health = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    description = db.Column(db.String(1024))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
