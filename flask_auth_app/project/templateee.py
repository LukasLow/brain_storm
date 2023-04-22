# auth.py

def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

@auth.route('/statistics', methods=['POST'])
@admin_role_required
def statistics_post():
    return render_template('statistics.html')

new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256", admin=False)

db.session.add(new_user)
db.session.commit()

list_of_seats = db.session.query(Seat).filter()
p = pd.DataFrame(data=list_of_seats)
p.to_csv()


# __init__

def open_file(filename):
    file_data_list = []
    file_data = open(filename)
    for line in file_data.read().splitlines():
        file_data_list.append(line.split())
    del file_data_list[0]
    return file_data_list

def load_seats():
    file = open_file("chartIn.txt")
    print(file)
    for line in range(0, len(file)):
        print("Reihe", line+1, "Sitz", file[line])
        for element in range(1, len(file[line])):
            print("Reihe", line+1, "Sitz", file[line][element])
            type = ""
            if element == 1 or element == 6:
                type = "Window seat"
            elif element == 2 or element == 5:
                type = "Middle seat"
            elif element == 3 or element == 4:
                type = "Aisle seat"
            seat = Seat(row=line+1, seat=file[line][element], reserved=-1, type=type)
            db.session.add(Seat, seat)
    db.session.commit()

load_seats()

        ### DB STUFF ###

## adding new or existing items

#user1 = User(name="user1")
#user2 = User(name="user2")
#session.add(user1)
#session.add(user2)

#session.commit()  # write changes to the database

#session.add_all([item1, item2, item3]) #add a list at once

## deleting

# mark two objects to be deleted
#session.delete(obj1)
#session.delete(obj2)

# commit (or flush)
#session.commit()


#my_user = session.get(User, 5)

## expiring refreshing
#>>> u1 = session.query(User).filter(id=5).first()
#>>> u2 = session.query(User).filter(id=5).first()
#>>> u1 is u2
#True