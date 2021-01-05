import flask
from application import app
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

# Used to create a room and store its creator
class Room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    admin = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __init__(self, admin, name):
        self.admin = admin
        self.name = name

# Used to see which rooms a person is in
class Groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __init__(self, room, user):
        self.room = room
        self.user = user

# Used to get posts based on the room
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable = False)

db.create_all()
    
