#Signin will handle the mechanics of signing a user in
from userManagement.Tokens import Tokens
import time
class Signin:

    def __init__(self, db):
        self.db = db
        self.token = Tokens()

    def validatePassword(self, username, password):
        print(self.db.validateUserExists(username))
        if(self.db.validateUserExists(username)):
            dbPassword = self.db.getPasswordFor(username)
            dbPassword = dbPassword[0][0]
		    #compare password to given getPassword
            if(password == dbPassword):
                return True
        return False

    def tokenUpToDate(self,username):
        tokenExpiration = self.db.getTokenCreationTime(username)
        #if(tokenExpiration):
        #    return False
        currentTime = time.time()
        print(tokenExpiration[0][0])
        timeDiference = currentTime - tokenExpiration[0][0]
        if(timeDiference > 86400):
            return False
        return True

    def signin(self, parsedData):
        username = parsedData["username"]
        password = parsedData["password"]
        if(self.validatePassword(username, password)):
            if(self.tokenUpToDate(username)):
                #Bundle the tocken into the response package
                signonToken = self.db.getToken(username)
                signonToken = signonToken[0][0]
                return signonToken
            else:
                signonToken = self.token.getToken()
                self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                print(signonToken)
                return signonToken
        return False

    def signout(self, parsedData, reqItem):
        username = parsedData["username"]
        signonToken = parsedData["signonToken"]

        savedToken = self.db.getToken()

        if(signonToken == savedToken):
            self.db.logout(username)
            reqItem.signoutResponse("success")
        else:
            reqItem.signoutResponse("failure")
