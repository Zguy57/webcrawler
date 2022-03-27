from replit import db
from extra import *
import json

Online = {}

class User():

        def __init__(self, username: str, password: str, history: str):
                self._username = username
                self._password = encrypt(username, password)
                self._history = history
                Online[username] = self

        def get_user(username: str, password: str):
                if username in db and json.loads(db[username])["_password"] == encrypt(username,password) and username[0] != "!":
                        user = json.loads(db[username])
                        return User(username, password, user["_history"])

        def register(username: str, password: str):
                if not username in db and username[0] != "@" and username[0] != "!":
                        db[username] = json.dumps(User(username, password, []).__dict__)
                        return True
                return False

        def log_scrape(self, event: str):
                self._history.append(event)
                db[self._username] = json.dumps(self.__dict__)

        def get_history(self):
                return self._history

        def get_username(self):
                return self._username

        def log_out(self):
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
        
      
