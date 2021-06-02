from flask.globals import session
import database as db

def login(username, password):
    is_valid_login = False
    user=None
    temp_user = db.get_user(username)
    if(temp_user != None):
        if(temp_user["password"]==password):
            is_valid_login=True
            user={"username":username,
                  "first_name":temp_user["first_name"],
                  "last_name":temp_user["last_name"]}
            
    return is_valid_login, user

def change_password_verification(old, new, confirm):
    old_is_correct = False
    new_is_same = False
    change_is_valid = False
    temp_user = db.get_user(session["user"]["username"])
    if(old == temp_user["password"]):
        old_is_correct = True
    if(new == confirm):
        new_is_same = True

    if old_is_correct and new_is_same:
        change_is_valid = True

    return old_is_correct, new_is_same, change_is_valid