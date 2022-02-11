from replit import db
from extra import *

class User():

        def __init__(self,username,password,history):
                self._username = username
                self._password = encrypt(username,password)
                self._history = history

        def get_user(username,password):
                if username in db and db[username][0] == encrypt(username,password):
                        return User(username,db[username][0],db[username][1])

        def register(username,password):
                if not username in db:
                        db[username] = [encrypt(username,password),[]]
                        return True
                return False

        def log_scrape(self,event):
                self._history.append(event)

        def get_history(self):
                return self._history
        
class Manager(User):

        def __init__(self,username,password):
                super().__init__(self,username,password)        

        
      
