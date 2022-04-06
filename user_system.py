from replit import db
from extra import *
import json
import re

Online = {}

SPECIAL_CHARACTERS = ("@", "!")
EMAIL_PATTERN = "[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+"

class User():
      
        def __init__(self, username: str, password: str, email: str, history: str):
                self._username = username
                self._password = encrypt(username, password)
                self._email = email
                self._history = history
                Online[username] = self

        def get_user(username: str, password: str):
                '''This is a class function that retrieves a User object if the username and the password match what is found on the replit database.'''
                if username in db and json.loads(db[username])["_password"] == encrypt(username,password) and username[0] != "!":
                        user = json.loads(db[username])
                        return User(username, password, user["_email"], user["_history"])

        def register(username: str, password: str, email: str):
                '''This is a class function that registers a new user if it does not exist on the replit database.'''
                if not username in db and username[0] not in SPECIAL_CHARACTERS and re.fullmatch(EMAIL_PATTERN, email):
                        db[username] = json.dumps(User(username, password, email, []).__dict__)
                        return True
                return False

        def log_scrape(self, event: str):
                '''This is an object function that logs a new scrape that a user made in the replit database.'''
                self._history.append(event)
                db[self._username] = json.dumps(self.__dict__)

        def get_history(self):
                '''This is an object function that retrieves a user's history.'''
                return self._history

        def get_username(self):
                '''This is an object function that retrieves a user's username.'''
                return self._username

        def get_email(self):
                '''This is an object function that retrieves a user's email.'''
                return self._email
          
        def log_out(self):
                '''This is an object function that logs out a user'''
                del Online[self._username]
        
class Manager(User):

        def __init__(self, username: str, password: str, history: str, management_history: str):
                super().__init__(self, username, password, history)
                self._management_history = management_history

        def set_manager(self, user: User):
                del db[user._name]
                db[f"@{user._name}"] = json.dumps(Manager(user._name, user._password, user._history, []).__dict__)
                self._management_history.append({"operation":"set_manager", "user":user._name})

        def delete_user(self, user: User):
                del db[user._name]
                self._management_history.append({"operation":"delete_user", "user":user._name})

        def ban_user(self, user: User):
                del db[user._name]
                db[f"!{user._name}"] = json.dumps(User(user._name, user._password, user._history).__dict__)
                self._management_history.append({"operation":"ban_user", "user":user._name})

        #undo operations needed
        
      
