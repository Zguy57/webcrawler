from replit import db
from extra import *
import re
import random
import datetime

Online = {}

EMAIL_PATTERN = "[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z\.0-9]+"

class Scrape:
  
        '''
          This class is used for representing a single scrape made by a user.

          Attributes:
            scrape_id: integer
              A unique 4-digit id given to a new scrape in order to help in finding it and differentiating it from other scrapes.
            content: dictionary
              The content of a scrape is stored as a dictionary such that the key is the name of an attribute in the scrape request and the value is a list of values stored in different objects at this attribute. (for example: {"url":["www.google.com","replit.com"], "bgcolor":["white","white"]})
        '''
  
        def __init__(self, scrape_id: int, content: dict):
                self._scrape_id = scrape_id
                self._content = content

        def get_id(self):
                '''This is an object function that returns the unique id of a scrape.'''
                return self._scrape_id

        def get_content(self):
                '''This is an object function that returns the content of a scrape.'''
                return self._content

        def log_scrape(content: dict):
                '''This function takes the content of a scrape and stores its data as an object.'''
                x = random.randint(1000,9999)
                while x in db["scrapes"]:
                        x = random.randint(1000,9999)
                scr = Scrape(x, content)
                db["scrapes"][str(x)] = scr.__dict__
                return str(x)

class User():

        '''
          This class is used for representing a user on the site.

          Attributes:
            username: str
              A unique username, that the user gave himself while he registered.
            password: str
              An encrypted password which is used for protecting the user account.
            email: str
              The user's email.
            history: list
              A list of scrape ids of the scrapes the user committed.
        '''
      
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

        def log_scrape(self, event: dict):
                '''This is an object function that logs a new scrape that a user made in the replit database.'''
                self._history.append(Scrape.log_scrape(event))
                db["users"][self._username] = self.__dict__

        def delete_scrape(self, scrape_id: str):
                '''This is an object function that deletes a scrape form the database.'''
                self._history.remove(scrape_id)
                db["users"][self._username] = self.__dict__
                del db["scrapes"][scrape_id]

        def get_history(self):
                '''This is an object function that retrieves a user's history.'''
                return [(db["scrapes"][x]["_content"], x) for x in self._history]

        def get_username(self):
                '''This is an object function that retrieves a user's username.'''
                return self._username

        def get_email(self):
                '''This is an object function that retrieves a user's email.'''
                return self._email

        def change_password(self, newpass):
                '''This is an object function that changes a user's password.'''
                self._password = encrypt(self._username, newpass)
                db["users"][self._username] = self.__dict__
          
        def log_out(self):
                '''This is an object function that logs out a user'''
                del Online[self._username]
                del self

class ManagerOperation:

        '''
          This class is used for representing a simple operation done by a manager.

          Attributes:
            operation: str
              The operation that the manager did.
            username: str
              The username of the user whom the operation was done on.
            time: str
              The time that the operation was done.
            operation_id: str
              A unique 4-digit id given to an operation in order to help in finding it and differentiating it from other operations.
        '''

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

        '''
          This class inherits functions and attributes from the user class, and it is used for representing a manager.

          Attributes:
            inherited: username, password, email, history.
            management_history: list
              A list of operation ids of operations done by a manager.
        '''

        def __init__(self, username: str, password: str, email: str, history: list, management_history: list):
                super().__init__(username, password, email, history)
                self._management_history = management_history

        def ban_user(self, username: str):
                '''This is an object function that bans a user and relates the ban to the manager.'''
                user = db["users"][username]
                db["banned"][username] = User(user["_username"], user["_password"], user["_email"], user["_history"]).__dict__
                del db["users"][username]
                x = random.randint(1000,2000)
                while x in db["operations"]:
                        x = random.randint(1000,2000)
                db["operations"][x] = ManagerOperation("ban_user", username, str(datetime.datetime.today()), x).__dict__
                self._management_history.append(x)

        def unban_user(self, username: str):
                '''This is an object function that unbans a user and relates the unban to the manager.'''
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
                self._history.append(Scrape.log_scrape(event))
                db["managers"][self._username] = self.__dict__

        def delete_scrape(self, scrape_id: str):
                self._history.remove(scrape_id)
                db["managers"][self._username] = self.__dict__
                del db["scrapes"][scrape_id]

        def set_manager(username: str):
                '''This is a class function that sets a new manager.'''
                user = db["users"][username]
                db["managers"][username] = Manager(user["_username"], user["_password"],  user["_email"], user["_history"], []).__dict__
                del db["users"][username]

        def reset():
                '''This function cleans the replit database.'''
                db["users"] = {}
                db["managers"] = {}
                db["operations"] = {}
                db["scrapes"] = {}
                db["banned"] = {}
      
