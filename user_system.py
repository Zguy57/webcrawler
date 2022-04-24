from replit import db
from extra import *
import json
import re
import random
import datetime

Online = {}

EMAIL_PATTERN = "[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+"



class User():
      
        def __init__(self, username: str, password: str, email: str, history: list):
                self._username = username
                self._password = password
                self._email = email
                self._history = history
                

        def get_user(username: str, password: str):
                '''This is a class function that retrieves a User object if the username and the password match what is found on the replit database.'''
                encrypted = encrypt(username,password)
                if username in db["users"] and db["users"][username]["_password"] == encrypted:
                        user = db["users"][username]
                        Online[username] = User(username, encrypted, user["_email"], user["_history"])
                        return Online[username]
                elif username in db["managers"] and db["managers"][username]["_password"] == encrypted:
                        user = db["managers"][username]
                        Online[username] = Manager(username, encrypted, user["_email"], user["_history"], user["_management_history"])
                        return Online[username]

        def register(username: str, password: str, email: str):
                '''This is a class function that registers a new user if it does not exist on the replit database.'''
                if not username in db["users"] and not username in db["managers"] and re.fullmatch(EMAIL_PATTERN, email):
                        db["users"][username] = User(username, encrypt(username, password), email, []).__dict__
                        return True
                return False

        def log_scrape(self, event: str):
                '''This is an object function that logs a new scrape that a user made in the replit database.'''
                self._history.append(event)
                db["users"][self._username] = self.__dict__

        def get_history(self):
                '''This is an object function that retrieves a user's history.'''
                return self._history

        def get_username(self):
                '''This is an object function that retrieves a user's username.'''
                return self._username

        def get_email(self):
                '''This is an object function that retrieves a user's email.'''
                return self._email

        def change_password(self, newpass):
            self._password = encrypt(self._username, newpass)
            db["users"][self._username] = self.__dict__
          
        def log_out(self):
                '''This is an object function that logs out a user'''
                del self

class ManagerOperation:

        def __init__(self, operation: str, username: str, time: str, operation_id: int):
                self._operation = operation
                self._username = username
                self._time = time
                self._operation_id = operation_id

        def __str__(self):
                toRet = f"<tr><th>Operation</th><td>{self._operation}</td></tr>" 
                toRet += f"<tr><th>User name</th><td>{self._username}</td></tr>" 
                toRet += f"<tr><th>Time</th><td>{self._time}</td></tr>"
                toRet += f"<tr><th>Operation id</th><td>{self._operation_id}</td></tr>" 
                return toRet

class Manager(User):

        def __init__(self, username: str, password: str, email: str, history: list, management_history: list):
                super().__init__(username, password, email, history)
                self._management_history = management_history

        def ban_user(self, username: str):
                user = db["users"][username]
                db["banned"][username] = User(user["_username"], user["_password"], user["_email"], user["_history"]).__dict__
                del db["users"][username]
                x = random.randint(1000,2000)
                while x in db["operations"]:
                        x = random.randint(1000,2000)
                db["operations"][x] = ManagerOperation("ban_user", username, str(datetime.datetime.today()), x).__dict__
                self._management_history.append(x)

        def unban_user(self, username: str):
                user = db["banned"][username]
                db["users"][username] = User(user["_username"], user["_password"], user["_email"], user["_history"]).__dict__
                del db["banned"][username]
                x = random.randint(1000,2000)
                while x in db["operations"]:
                        x = random.randint(1000,2000)
                db["operations"][x] = ManagerOperation("unban_user", username, str(datetime.datetime.today()), x).__dict__
                self._management_history.append(x)

        def change_password(self, newpass):
              self._password = encrypt(self._username, newpass)
              db["managers"][self._username] = self.__dict__

        def log_scrape(self, event: str):
                '''This is an object function that logs a new scrape that a user made in the replit database.'''
                self._history.append(event)
                db["managers"][self._username] = self.__dict__

        def cmd_manager(username: str):
                user = db["users"][username]
                db["managers"][username] = Manager(user["_username"], user["_password"],  user["_email"], user["_history"], []).__dict__
                del db["users"][username]

        def reset():
                db["users"] = {}
                db["managers"] = {}
                db["operations"] = {}
      
