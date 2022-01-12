import json

class User():

        def __init__(self,username,password):
                self.__username__ = username
                self.__password__ = User.__encrypt__(username,password)

        def __encrypt__(username,password):
                toRet = ""
                for i in range(len(password)):
                        toRet += chr((ord(password[i])+1)^(ord(username[i%len(username)])))
                return toRet

        def auth(self,username,password):
                return (self.__username__ == username and self.__password__ == User.__encrypt__(username,password))

class Manager(User):

        def __init__(self,username,password):
                super().__init__(self,username,password)

        

        
      
