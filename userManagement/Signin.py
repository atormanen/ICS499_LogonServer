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

    def signin(self, parsedData, reqItem):
        username = parsedData["username"]
        password = parsedData["password"]
        data = self.getAccountInfo(parsedData)

        if(self.validatePassword(username, password)):
            if(self.tokenUpToDate(username)):
                #Bundle the tocken into the response package
                signonToken = self.db.getToken(username)
                signonToken = signonToken[0][0]
                print(signonToken)
                if(signonToken == 'null'):
                    signonToken = self.token.getToken()
                    self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                reqItem.signinResponse(token, data)
            else:
                signonToken = self.token.getToken()
                self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                print(signonToken)
                reqItem.signinResponse(token, data)
        return False

    def signout(self, parsedData, reqItem):
        username = parsedData["username"]
        signonToken = parsedData["signonToken"]
        print(parsedData)

        savedToken = self.db.getToken(username)

        self.db.logout(username)
        self.db.saveAccountInfo(username, parsedData)
        reqItem.signoutResponse("success")


    def getAccountInfo(self, parsedData):
        username = parsedData["username"]
        #signonToken = parsedData["signonToken"]
        data = self.db.getAccountInfo(username)
        print(data)
        return data
