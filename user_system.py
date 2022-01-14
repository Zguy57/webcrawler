import json

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

        def getuser(username,password):
                with open("users.json","r") as usersfile:
                        users = json.load(usersfile)
                        try:
                                password2 = users[username][0]
                                if password == password2:
                                        return User(usename,password,users[username][1])
                                else:
                                        return None
                        except:
                                return None

        def register(username,password):
                users = None
                with open("users.json","r") as usersfile:
                        users = json.load(usersfile)
                users.append({username:[User.__encrypt(username,password),[]]})
                with open("users.json","w") as usersfile:
                        json.dump(users,usersfile,indent=2)

        def log_scrape(self,event):
                self._history.append(event)

        def get_history(self):
                return self._history
        
class Manager(User):

        def __init__(self,username,password):
                super().__init__(self,username,password)        

        
      
