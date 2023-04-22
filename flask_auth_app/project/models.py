# this file contains the user and seat model
from flask_login import UserMixin
# import database to define the columns using classes
from . import db

#User model to store information about users
class User(UserMixin, db.Model):
    # column for primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    # column for the email, unique for each user
    email = db.Column(db.String(100), unique=True)
    # column for the password
    password = db.Column(db.String(100))
    # column for the name
    name = db.Column(db.String(1000))
    # column for the admin status
    admin = db.Column(db.Boolean())


# seat model to store information about seats
class Seat(db.Model):
    # column for primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    # column for the row number
    row = db.Column(db.Integer())
    # column for the seat letter
    seat = db.Column(db.String(1))
    # column for the seat type
    type = db.Column(db.String(100))
    # column for the user id of the user who reserved the seat
    reserved_id = db.Column(db.Integer())