# import necessary modules to send emails
from email.mime.text import MIMEText
import smtplib
# import necessary modules from flask and flask-Login
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, make_response, send_file, Flask
from flask_login import login_user, login_required, logout_user, current_user
# import database from current folder (flask_auth_app)
from . import db
# import seat and user class from the models.py in (flask_auth_app/project) 
from .models import User
from project.models import Seat, User
# needed for the admin check
from functools import wraps
# needed for hashing the password
from werkzeug.security import generate_password_hash, check_password_hash
import os

auth = Blueprint('auth', __name__)

# The Class for sending Emails
class Email:
    # This defines the used SMTP server and the user credentials
    def __init__(self, smtp_address, smtp_port, smtp_user, smtp_password):
        self.smtp_address = smtp_address
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    # This function can be used to send the Eamil
    def send_email(self, email_text, email_subject, email_sender, email_receiver):
        # Creating a MIMEText object with the email text
        msg = MIMEText(email_text)
        # Setting the subject, sender, and receiver
        msg['Subject'] = email_subject
        msg['From'] = email_sender
        msg['To'] = email_receiver
        # Connecting to the SMTP server and logging in using the provided credentials
        with smtplib.SMTP(self.smtp_address, self.smtp_port) as server:
            server.login(self.smtp_user, self.smtp_password)
            # Sending the email
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            
# This can't be on Github
#email = Email("______server______", 587, "______username______", "______PASSWORD______")
#email.send_email("email_text", "email_subject", "email_sender", "email_receiver")


#this is a function for
def create_seat_chart(seats_query):
    seats = [] # create an empty list to store the seat data
    
    # loop through all seats and check if reserved, if so change the value to 'X'
    for x in seats_query: 
        if x.reserved_id != -1: # check if the seat is reserved
            x.seat = 'X' # if it is mark it as 'X'
        seats.append(x.seat) # update seat letter to the seats list

    seat_chart = []  # create an empty list to store the seat chart data row by row
    liste = []  # create an empty list to store each row individually
    i = 1 # variable to count rows
    while seats != []:
        liste.append(i) # append the row number
        liste.append(' '.join(seats[:3])) # append the first 3 seats
        liste.append('|   |') # append a separator
        seats = seats[3:] # remove 3 seats from the seats list
        liste.append(' '.join(seats[:3])) # append the next 3 seats
        seats = seats[3:] # remove 3 seats from the seats list
        seat_chart.append(liste) # append the row to the seat chart
        liste = [] # reset the list
        i += 1 # increase the row number by 1
    return seat_chart
# To use it: create_seat_chart(Seat.query.all())


# DEFINE ADMIN ROLE
EXEMPT_METHODS = {"OPTIONS"} # this line is setting a set containing the string "OPTIONS"
def admin_role_required(func):
    @wraps(func)  # this line is using the wraps function to preserve the metadata of the original function
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:  # this line is checking if the current request method is in the EXEMPT_METHODS set
            return func(*args, **kwargs)
        # if the user is not an admin, the request is aborted with a 403 status code
        elif not current_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view 


# this function renders the login template when the user navigates to the login page.
@auth.route('/login')
def login():
    return render_template('login.html')


# this function handles the login process when the user submits the login form.
@auth.route('/login', methods=['POST']) # adds POST method to retrieve information from webpage
def login_post():
    # get the user-supplied email and password from the page
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # find the user in the database
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    # redirect to the profile page
    return redirect(url_for('main.profile'))


# this function renders the signup template when the user navigates to the signup page.
@auth.route('/signup')
def signup():
    return render_template('signup.html')


# this function handles the sign-in process when the user submits the sign-in form.
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # check if the email already exists in the database
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(
        password, method='sha256'), admin=False)

    # add the new user to the database
    db.session.add(new_user)
    # save all changes to the database
    db.session.commit()
    # redirect the user to the login page
    return redirect(url_for('auth.login'))




# this function renders the booking template when the user navigates to the booking page.
@auth.route('/booking')
@login_required # with this only logged-in users can access this webpage
def booking():
    return render_template('booking.html', liste=create_seat_chart(Seat.query.all())) # return seat chart


# this function handles the booking process when the user submits the booking form.
@auth.route('/booking', methods=['POST'])
@login_required # with this only logged in users can access this webpage
def booking_post():
    seatnumber = request.form.get('seat') # Get seat number from the form
    # Split the seat number into row and seat
    ROW = seatnumber[:-1] # Extract row number from seatnumber
    SEAT = seatnumber[-1] # Extract seat letter from seatnumber
    SEAT = SEAT.upper() # convert lowercase to uppercase in case user puts in lowercase
    # Define the possible values of rows and seats
    ex_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    ex_seats = ['A', 'B', 'C', 'D', 'E', 'F']
    message = "" # Initialize the message as an empty string for probable errors

    # Check if the seat number entered is valid
    if ROW not in ex_rows or SEAT not in ex_seats:
        message = "SEAT DOESN'T EXIST"
    else:
        email = current_user.email # Get email of the current user
        u = db.session.query(Seat).filter(Seat.row == ROW, Seat.seat == SEAT).first() # Get seat object corresponding to the entered seat number
        v = db.session.query(User).filter(User.email == email).first() # Get user object corresponding to the current user email
        # Check if the seat is available
        if u.reserved_id == -1:
            # Reserve the seat for the current user
            u.reserved_id = v.id
            # save changes to the database
            db.session.commit()
            message = "SEAT RESERVED SUCCESSFULLY" # confirmation message
        # If the seat is reserved give error message SEAT UNAVAILABLE
        elif u.reserved_id != -1:
            message = "SEAT UNAVAILABLE"
    # Render the booking template with the message and seat chart
    return render_template('booking.html', message=message, liste=create_seat_chart(Seat.query.all()))


# this function renders the cancel template when the user navigates to the cancel page.
@auth.route('/cancel')
@admin_role_required # the user needs admin role to access or he will abort with 403
def cancel():
    return render_template('cancel.html', liste=create_seat_chart(Seat.query.all()))


# this function handles the canceling process when the user submits the canceling form.
@auth.route('/cancel', methods=['POST'])
@admin_role_required # the user needs admin role to access or he will abort with 403
def cancel_post():
    seatnumber = request.form.get('seat') # Get the seat number from the form
    # Split the seat number into row and seat
    ROW = seatnumber[:-1] # Extract row number from seatnumber
    SEAT = seatnumber[-1] # Extract seat letter from seatnumber
    SEAT = SEAT.upper()  # convert lowercase to uppercase in case user puts in lowercase
    # Define the possible values of rows and seats
    ex_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    ex_seats = ['A', 'B', 'C', 'D', 'E', 'F']
    message = "" # Initialize the message as an empty string


    # Check if the seat exists
    if ROW not in ex_rows or SEAT not in ex_seats:
        message = "SEAT DOESN'T EXIST"
    else:
        email = current_user.email # Get email of the current user
        # get the seat and user from the database
        u = db.session.query(Seat).filter(Seat.row == ROW, Seat.seat == SEAT).first()  # Get the seat with the specified row and seat
        v = db.session.query(User).filter(User.email == email).first() # Get the user with the specified email
        # check if the seat is occupied
        if u.reserved_id == -1:
            message = "SEAT NOT OCCUPIED"
        elif u.reserved_id != -1:
            # cancel the reservation
            u.reserved_id = -1
            # save all changes to the database
            message = "SEAT CANCELED SUCCESSFULLY"  # confirmation message
            db.session.commit()
    # render the cancel template with the message and seat chart
    return render_template('cancel.html', message=message, liste=create_seat_chart(Seat.query.all()))


# this function handles when the user goes to /statistics
@auth.route('/statistics')
@admin_role_required # the user needs admin role to access or he will abort with 403
def statistics():
    SITZE = Seat.query.all() # load all seats and store it as a variable "SITZE"
    USERS = User.query.all() # load all users and store it as a variable "USERS"

    num_seats = 0 # create a variable to store the number of seats
    num_available = 0 # create a variable to store the number of available seats
    per_available = 0 # create a variable to store the percentage of available seats
    num_reserved = 0 # create a variable to store the number of reserved seats
    per_reserved = 0 # create a variable to store the percentage of reserved seats
    list_available = [] # create a list to store the available seats
    list_reserved = [] # create a list to store the reserved seats
    num_users = 0 # create a variable to store the number of users
    list_users = []  # create a list to store all users

    # loop through all seats and count the number of available and reserved seats
    for x in SITZE:
        num_seats += 1 # count number of all seats
        if x.reserved_id != -1: # if the seat is reserved
            num_reserved += 1 # increase the number of reserved seats by 1
            list_reserved.append("%s%s" % (x.row, x.seat)) # add the reserved seat to the list of reserved seats
        elif x.reserved_id == -1: # if the seat is available
            num_available += 1 # increase the number of available seats by 1
            list_available.append("%s%s" % (x.row, x.seat)) # add the available seat to the list of available seats
            
    # loop through all users and count the number of users
    for y in USERS:
        num_users += 1 # increase the number of users by 1
        list_users.append("ID: %s EMAIL: %s NAME: %s" %(y.id, y.email, y.name)) # add the user info to the list of users

    per_available = (num_available / num_seats) * 100 # calculate the percentage of available seats
    per_reserved = (num_reserved / num_seats) * 100 # calculate the percentage of reserved seats

    # render the statistics page and its necessary variables
    return render_template('statistics.html', num_available=num_available, per_available=per_available,
                           num_reserved=num_reserved, per_reserved=per_reserved, list_reserved=list_reserved,
                           list_available=list_available, num_users=num_users, list_users=list_users)


# this function handles when the user goes to /statistics and presses the save to file button and get redirects to /save_to_file
@auth.route('/save_to_file')
@admin_role_required # the user needs admin role to access or he will abort with 403
def save_to_file():
    SITZE = Seat.query.all() # load all seats and store it as a variable "SITZE"
    USERS = User.query.all() # load all users and store it as a variable "USERS"

    num_seats = 0 # create a variable to store the number of seats
    num_available = 0 # create a variable to store the number of available seats
    per_available = 0 # create a variable to store the percentage of available seats
    num_reserved = 0 # create a variable to store the number of reserved seats
    per_reserved = 0 # create a variable to store the percentage of reserved seats
    list_available = [] # create a list to store the available seats
    list_reserved = [] # create a list to store the reserved seats
    num_users = 0 # create a variable to store the number of users
    list_users = []  # create a list to store all users

    # loop through all seats and count the number of available and reserved seats
    for x in SITZE:
        num_seats += 1 # increase the number of seats by 1
        if x.reserved_id != -1: # if the seat is reserved
            num_reserved += 1 # increase the number of reserved seats by 1
            list_reserved.append("%s%s" % (x.row, x.seat)) # add the reserved seat to the list of reserved seats
        elif x.reserved_id == -1: # if the seat is available
            num_available += 1 # increase the number of available seats by 1
            list_available.append("%s%s" % (x.row, x.seat)) # add the available seat to the list of available seats
            
    # loop through all users and count the number of users
    for y in USERS:
        num_users += 1 # increase the number of users by 1
        list_users.append("ID: %s EMAIL: %s NAME: %s" %(y.id, y.email, y.name)) # add the user details to the list of users

    per_available = (num_available / num_seats) * 100 # calculate the percentage of available seats
    per_reserved = (num_reserved / num_seats) * 100 # calculate the percentage of reserved seats

    # combine all statistics into a single string
    data_stats = "Here's some statistics :)\n"+"\nNumber of available seats: " + \
        str(num_available) + "\nPercentage of available seats: " + str(per_available) + "%" +\
        "\nNumber of reserved seats: " + str(num_reserved) +\
        "\nPercentage of reserved seats: " + str(per_reserved) + "%" +\
        "\nList of available seats: " + str(list_available) +\
        "\nList of reserved seats: " + str(list_reserved) +\
        "\nHere's the number of users: " + str(num_users) +\
        "\nHere's a list of the users " + str(list_users)

    # save the string to a file
    with open('data_stats.txt', 'w') as f:
        f.write(data_stats)

        # create a response object with the file as an attachment
        response = make_response(data_stats)
        # set the header for the response object to include the filename
        response.headers["Content-Disposition"] = "attachment; filename=data_stats.txt"
        # return the response object
        return response


@auth.route('/logout')
@login_required
def logout():
    logout_user() # log out the user
    # message to display after successful log out
    message = "You have been successfully logged out. Thank you for choosing our services today. We <3 you!"
    flash(message) # flash the message to be displayed in the next request
    # redirect the user to the login page
    return redirect(url_for('auth.login'))