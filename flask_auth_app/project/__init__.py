# this file sets up the app
from datetime import timedelta
import sys
import sqlalchemy
from werkzeug.security import generate_password_hash
import os
# import necessary modules from flask and flask-Login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# Adding a function to add Users
def load_users(db):
    # Gets from the models.py file the User class
    from project.models import User
    # create 4 users to put into database
    admin = User(email="admin@test.com", name="admin",
                 password=generate_password_hash("1234", method="sha256"), admin=True)
    user1 = User(email="user1@test.com", name="user1",
                 password=generate_password_hash("2", method="sha256"), admin=False)
    user2 = User(email="user2@test.com", name="user2",
                 password=generate_password_hash("3", method="sha256"), admin=False)
    user3 = User(email="user3@test.com", name="user3",
                 password=generate_password_hash("4", method="sha256"), admin=False)
    # adding all user from above to the database
    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    # save all changes to the database
    db.session.commit()

# Adding a function to open a text file
def open_file(filename):
    """
    This function opens the specified file, reads its contents line by line, and stores each line as a list of words in a list.
    The first line of the file is ignored.
    :param filename: The name of the file to be opened.
    :return: A list of lists, where each list contains the words from a line of the file.
    """
    # Initialize an empty list to store the file data
    file_data_list = []
    # Open the file using the passed filename
    file_data = open(filename)
    # Read the file, split the lines and append them to the file_data_list
    for line in file_data.read().splitlines():
        file_data_list.append(line.split())
    # Remove the first element of the list (the row numbers)
    del file_data_list[0]
    # Return the final list
    return file_data_list


# Adding a function to load the Seats
def load_seats(db):
    # Import from the models.py the Seat class
    from project.models import Seat
    # Set the variable "file" to the text in the file "chartIn.txt"
    file = open_file("./project/chartIn.txt")
    # loop through the file data
    for line in range(0, len(file)):
        # loop through the seats in each row
        for element in range(1, len(file[line])):
            # determine the seat type based on its position in the row
            type = ""
            if element == 1 or element == 6:
                type = "Window seat"
            elif element == 2 or element == 5:
                type = "Middle seat"
            elif element == 3 or element == 4:
                type = "Aisle seat"
            # create a new seat object with attributes row, seat, id and type
            seat = Seat(row=line+1, seat=file[line]
                        [element], reserved_id=-1, type=type)
            # adding the seats to the database
            db.session.add(seat)
    # save all changes to the database
    db.session.commit()

# Initialize the Flask application and it's settings
def create_app():
    # Create a Flask application instance
    app = Flask(__name__)
    # Set the session lifetime to 600 seconds
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=600)
    # Set a secret key for the application
    app.config['SECRET_KEY'] = 'v7DppDWLrAlBU7ecwKfaIDcs0mAKuXIU'
    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize the database with the app
    db.init_app(app)

    # Create a login manager for handling authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # import classes user and seat from models
    from project.models import User, Seat

    # Define a function to load a user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Creating the database and loading data
    with app.app_context():
        # Create all the tables defined in the models
        db.drop_all()
        db.create_all()
        # try to load users and seats with given database db
        try:
            load_users(db)
            load_seats(db)
        except sqlalchemy.exc.IntegrityError:
            pass

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
