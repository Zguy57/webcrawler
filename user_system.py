from replit import db

class User():

        def __init__(self,username,password,history):
                self._username = username
                self._password = User.__encrypt(username,password)
                self._history = history

        def __encrypt(username,password):
                toRet = ""
                for i in range(len(password)):
                        toRet += chr((ord(password[i])+1)^(ord(username[i%len(username)])))
                return toRet

        def get_user(username,password):
                if db[username] and db[username][0] == User.__encrypt(username,password):
                        return User(username,db[username][0],db[username][1])

        def register(username,password):
                if not db[username]:
                        db[username] = [User.__encrypt(username,password),[]]

        def log_scrape(self,event):
                self._history.append(event)

        def get_history(self):
                return self._history
        
class Manager(User):

        def __init__(self,username,password):
                super().__init__(self,username,password)        

        
      
