# import necessary modules from flask and flask-Login
import os
from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user
# import database from current folder (flask_auth_app)
from . import db
# import seat class from the models.py in (flask_auth_app/project)
from project.models import Seat
# create a blueprint named "main"
main = Blueprint('main', __name__)

# route for the index page
@main.route('/')
def index():
    return render_template('index.html')


# route for the profile page
@main.route('/profile')
@login_required # require the user to be logged in to access this page
def profile():
    SITZE = Seat.query.all() # get all seat objects from the database
    user_seats = [] # list to store the user's reserved seats

    for x in SITZE: # loop through all seats in the database
        if x.reserved_id == current_user.id: # check if the current seat is reserved by the current user
            user_seats.append("%s%s %s" % (x.row, x.seat, x.type)) # if true add the seat to the list of current user's reserved seats

    # render the template for the profile page with the current username, email, and reserved seats
    return render_template('profile.html', name=current_user.name, email=current_user.email, user_seats=user_seats)


# route for the help page
@main.route('/help')
def help():
    return render_template('help.html')

# route to send files from the assets folder
@main.route('/assets/<path:path>')
def send_files(path):
    return send_from_directory('./templates/assets', path)

# @main.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(main.root_path, 'static'),'favicon.ico', mimetype='./templates/assets/pic')

