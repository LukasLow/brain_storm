# Airline Website "Lowsky.eu"

## A short description of the project’s purpose 

This project represents an interactive website of a fictitious airline where users can log in and log out after registration. Users can then book individual seats which are then no longer available to other users. Only admins can cancel the bookings and also view statistics. There is a help button that provides information of how to use the features of the website.

## Motivation

The project was created as part of the final exam for the course "Programmieren für Data Scientists: Python" by the group "brain_storm". It serves as a practical application of the contents learned during the semester on basics in Python coding.

## Features

Our project stands out as it enables the user to experience an authentic booking and reserve program for airplane seats. 

Unique features our program offers include the following: 

- a beautiful welcome page 
![](https://github.com/sosonjaa/brain_storm/raw/main/flask_auth_app/project/templates/assets/pic/plane.png)
- confirmation of succesfull sign up via email
![](https://github.com/sosonjaa/brain_storm/raw/main/flask_auth_app/project/templates/assets/pic/email_signup.jpeg)
- individual greeting of each user
![](https://github.com/sosonjaa/brain_storm/raw/main/flask_auth_app/project/templates/assets/pic/individual_greeting.png)
- individual seat booking
- available seats are shown on the screen, whereas reserved seats are marked with an X
- seat charts are automatically updated after reservation/cancelation
- the user is able to confirm his/her choice by clicking on a button
- a confirmation email sent after successfull seat bookings
- statistics on seats and users available only for admins 
- statistics are available as a text file for download
- automatic log out after 5 minutes of inactivity
- a thank you message is displayed after the user logs out
![](https://github.com/sosonjaa/brain_storm/raw/main/flask_auth_app/project/templates/assets/pic/logout_message.png)
- help button to navigate through the website
![](https://github.com/sosonjaa/brain_storm/raw/main/flask_auth_app/project/templates/assets/pic/help_buttons.png)



Ideen: screenshots von der mainpage der Website + brain_storm logo.

## Code examples
This code is a python script using the Flask web framework to define a route for a profile page. It starts by using the @main.route decorator to specify the URL for the profile page as /profile. The @login_required decorator requires the user to be logged in to access this page.

The profile function retrieves all the Seat objects from the database using the Seat.query.all() method and stores them in the SITZE variable. It then creates an empty list user_seats to store the seats reserved by the current user.

The function then loops through all the seats in the SITZE list, checking if each seat is reserved by the current user by comparing x.reserved_id with current_user.id. If the current seat is reserved by the current user, the seat information is added to the user_seats list in the format of row + seat + type.

Finally, the render_template function is used to render the profile.html template, passing the current username, email, and reserved seats as variables.

```python
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
```

----

This code is a python script that adds users to a database using the SQLAlchemy ORM.

The load_users function takes a db argument, which is an instance of the SQLAlchemy object. The function starts by importing the User class from the project.models file.

Then, four User objects are created and stored in the admin, user1, user2, and user3 variables. The email, name, and password fields of each user are set and the admin field is set to True for the admin user and False for the other users. The password is hashed using the generate_password_hash method and the hash method used is sha256.

Finally, the db.session.add method is used to add each user to the database session and the db.session.commit method is used to save the changes to the database.

```python
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
```

## Installation

Install this repo with git

```bash
  git clone https://github.com/sosonjaa/brain_storm.git
```

```bash
  cd brain_storm && cd flask_auth_app
```

```bash
  python3 -m venv auth
```

```bash
  source auth/bin/activate
```

```bash
  pip install flask flask-sqlalchemy flask-login
```

```bash
  flask --app project run
```
  

## Webserver deployment


```bash
  sudo apt update && sudo apt upgrade
```

```bash
  cd /var/www/
```

```bash
  git clone https://github.com/sosonjaa/brain_storm.git
```

```bash
  cd /var/www/flask_auth_app
```

```bash
   pip install gunicorn
```


```bash
  gunicorn -w 4 -b lowsky.eu:80  'project.__init__:create_app()'
```


## Authors

- Inga von Freytag Löringhoff ([@XiaoMaomify](https://github.com/XiaoMaomify))
- Valentina Hoffmann ([@hvalentina](https://github.com/hvalentina))
- Lukas Lowschizky ([@LukasLow](https://github.com/LukasLow))
- Sonja Siekmann ([@sosonjaa](https://github.com/sosonjaa))


## License


Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file LICENSE.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License

----

# Todo-list

## Objective

The goal of this project is to implement a seat reservation system for an airplane consisting of:

* A relational database for data storage
* A web-based frontend
* A computing backend implemented in Python

## Requirements

The system should offer the following functionality.  We list the minimal functionality required for a passing grade marked with [!]and several options to improve the system and achieve a better grade for the course marked with [*]. You are welcome to include other useful features beyond our suggestions to further improve the system.

### Input Data

* [x] [!] The system must be able to read data from a text file “chartIn.txt” that represents a seat chart.
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa)  & [Valentina](https://github.com/sosonjaa) set up the feature to open and work with the data provided by text files
> * [Valentina](https://github.com/hvalentina)
> 
> * Created chartIn.txt file
> * open txt file and read seat chart data from it
> * transfer seat data into database using SQLAlchemy

### Login, Logout

* [x] [!] Users must be able to login into the system via the web interface.

> [Lukas](https://github.com/LukasLow)
>  
> * Created a login route and associated template
> * Implemented a POST method for the login route to handle user authentication
> * Retrieved user email and password from the login form
> * Checked if the user exists in the database by querying the User table using the email provided
> * Hashed the user-supplied password and compared it to the hashed password in the database
> * If the user doesn't exist or password is wrong, displayed an error message and redirected the user to the login page
> * If the user's credentials are correct, logged the user in and redirect them to their profile page.
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) updated the auth.py by implementing the basic POST-method in the sign-up function and the login function
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) further updated the sign-up function by handling the users input and check the databank for existing user. A flash message is displayed once the given input already exists.

* [x] [!] The database should contain at least 4 user accounts with the following information:  userID, name, user_name, password. Only these users are allowed to enter the system. One of the users should have admin privileges in your system (explained later).
> * [Lukas](https://github.com/LukasLow) Define the User model class
> * [Lukas](https://github.com/LukasLow) Create the database tables for the User model
> * [Lukas](https://github.com/LukasLow) Add a new user to the database
* [x] [!] The system offers a logout button. When users click it, the system displays a thank you message and quits after a timeout period.
  
> * [Lukas](https://github.com/LukasLow) Implemented a logout route that can only be accessed by logged in users
> * [Lukas](https://github.com/LukasLow) Included a login_required decorator to ensure that only logged in users can access the route
> * [Lukas](https://github.com/LukasLow) Called the logout_user() function to log the user out of their session
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) Displayed a message to the user indicating that they have been successfully logged out
> * [Lukas](https://github.com/LukasLow) Redirected the user to the login page

### Display Seats

* [x] [!] The system displays a basic seat chart consisting of only letters grouped into two equally-sized groups for left and right, pie symbols and whitespace between the groups to represent the aisle, e.g., A B C |   | DE F.
* [x] [!] The system shows available seats by showing the seat letter and occupied seats using X, e.g., XX C |   | X E F.
> [Valentina](https://github.com/hvalentina)
> 
> * created function for seat chart creation that can be passed to html files
> * created displayal of seat chart in html
> * replaced seat letters by 'X' using id of seats


### Reserve/Cancel Seats

* [x] [!] Users can reserve seats by entering the seat number, e.g., 4Ainto a dialog field.  If the seat is already occupied, an error message is displayed.  Every action should be confirmed by the user before being committed. Once confirmed, the information is automatically updated in the database and the interface. Only the admin user can cancel a reservation. After a reservation is canceled, the seat becomes available, again.
> [Valentina](https://github.com/hvalentina)
> 
> * take seat value from html site and look it up in database
> * reserve seat in database or display error if seat is occupied
> * error for wrong input added
> * confirmation button and message
> * displayal of reserved seats and seat type in user profile
* [x] [*] The system sends a conformation email for reserved seats.
  
> [Lukas](https://github.com/LukasLow)
>  
> * Created a class named Email
> * Defined an init method that takes 4 parameters: smtp_address, smtp_port, smtp_user, and smtp_password. These parameters are used to configure the SMTP server and user credentials for sending emails.
> * Defined a send_email method that takes 4 parameters: email_text, email_subject, email_sender, and email_receiver. This method is used to send the email.
> * Within the send_email method, created a MIMEText object with the email text provided
> * Set the subject, sender, and receiver for the email using the email_subject, email_sender, and email_receiver parameters respectively.
> * Established a connection to the SMTP server using the smtplib library and the address and port provided in the init method.
> * Only uncommet now in the code. Becouse my password can't be on Github and the code would crash.

### Statistics

* [x] [!] The system offers a statistics area exclusively for admin users. The options in this area or menu should at least include the following statistics that can be saved into a text file
  * [x] Number and percentage of available seats
  * [x] Number and percentage of reserved seats
  * [x] List of seats that are available
  * [x] List of seats that are not available
  * [x] Number of users in the system with their information, except for their password
> * [Valentina](https://github.com/hvalentina) created and calculated demanded values, passed on to html
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) implemented a statistics button and the feature that only admins can see the statistics button 
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) added the feature that the statistics can be downloaded as a text file by admin users only


### Help

* [x] [!] The system offers a help page that describes how to use the system and all its options

> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) initiated the help page 
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) implemented four popup buttons on the help page to answer possible questions by the user


### Coding Practices (all mandatory)

* [X] During the final presentation, enable the teaching team to test a working prototype, either on your machine or better running online.

> [Lukas](https://github.com/LukasLow)
>
> * Explained above

* [ ] Structure your source code appropriately into classes according to OOP principles.
* [ ] Adhere to the PEP 8 Style Guide and best practice guidelines
* [ ] Handle errors properly, so the system does not crash.
* [ ] Include unit tests for all methods that read in data from external sources or user input and all methods that manipulate data.

> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) updated the user models to add flask-login attributes 
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) iadded the feature that the user is remembered after logging in
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) imported login_required to check if user is locked in 
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) initiated current_user class
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) set up the feature to log out by clicking on the logout button 
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) & [Lukas](https://github.com/sosonjaa) created a readme file
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) & [Valentaina](https://github.com/sosonjaa) & [Lukas](https://github.com/sosonjaa) added inline comments
> * [Inga](https://github.com/XiaoMaomify) & [Sonja](https://github.com/sosonjaa) group coordination
