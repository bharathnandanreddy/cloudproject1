from . import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    filename = db.Column(db.String(1000))
    count=db.Column(db.String(1000))
    fname = db.Column(db.String(1000))
    lname = db.Column(db.String(1000))