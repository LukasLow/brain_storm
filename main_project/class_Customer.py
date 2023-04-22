class Customer:
    def __init__(self):
        self.users = [
            {"userID": 1, "name": "Pam", "user_name": "Beesly123", "password": "password1", "admin": False},
            {"userID": 2, "name": "Jim", "user_name": "Jimbo456", "password": "password2", "admin": False},
            {"userID": 3, "name": "Oscar", "user_name": "Wilde789", "password": "password3", "admin": False},
            {"userID": 4, "name": "Angela", "user_name": "sprinkles101", "password": "password4", "admin": False}
        ]

    def add_user(self, userID, name, user_name, password, admin=False):
        new_user = {"userID": userID, "name": name, "user_name": user_name, "password": password, "admin": admin}
        self.users.append(new_user)
        return f"User {name} with userID {userID} has been added"

    def delete_user(self, userID):
        for user in self.users:
            if user["userID"] == userID:
                self.users.remove(user)
                return f"User with userID {userID} has been removed"
        return f"User with userID {userID} not found"

    def update_user(self, userID, name=None, user_name=None, password=None):
        for user in self.users:
            if user["userID"] == userID:
                if name:
                    user["name"] = name
                if user_name:
                    user["user_name"] = user_name
                if password:
                    user["password"] = password
                return f"User with userID {userID} has been updated"  # indentation wrong?
            else:
                return f"User with userID {userID} not found"   # indentation wrong?

    def get_user(self, userID=None, user_name=None):
        for user in self.users:
            if userID and user["userID"] == userID:
                return user
            if user_name and user["user_name"] == user_name:
                return user
        return f"User not found"


customers = Customer()

print(customers.users)
customers.add_user(5, "Michael", "Mike<3", "password6")
print(customers.users)

print(customers.get_user(user_name="Mike<3"))


# delete admin class
class Admin(Customer):
    def cancel_reservation(self, userID, reservation_id):
        for user in self.users:
            if user["userID"] == userID:
                if user["admin"] == True:
                    # Code to cancel the reservation has to be added here
                    return f"Reservation {reservation_id} has been canceled by admin user {user['name']} with userID {userID}"
                else:
                    return f"User {user['name']} with userID {userID} is not authorized to cancel reservations"
        return f"User with userID {userID} not found"

admin = Admin()
admin.users[0]['admin'] = True
print(admin.cancel_reservation(1, "R1234"))

