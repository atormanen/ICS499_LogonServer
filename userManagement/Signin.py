from global_logger import logger, VERBOSE
import inspect

#Signin will handle the mechanics of signing a user in
from userManagement.Tokens import Tokens
import time
class Signin:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, db):
        self.db = db
        self.token = Tokens()

    def validatePassword(self, username, password):
        self.log_function_name()
        if(self.db.validateUserExists(username)):
            dbPassword = self.db.getPasswordFor(username)
            dbPassword = dbPassword[0][0]
		    #compare password to given getPassword
            if(password == dbPassword):
                return True
        return False

    def tokenUpToDate(self,username):
        self.log_function_name()
        tokenExpiration = self.db.getTokenCreationTime(username)
        #if(tokenExpiration):
        #    return False
        currentTime = time.time()
        timeDiference = currentTime - tokenExpiration[0][0]
        if(timeDiference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True

    def signin(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        password = parsedData["password"]
        data = self.getAccountInfo(parsedData)

        if(self.validatePassword(username, password)):
            if(self.tokenUpToDate(username)):
                #Bundle the tocken into the response package
                signonToken = self.db.getToken(username)
                signonToken = signonToken[0][0]
                logger.debug(type(signonToken))
                if(signonToken == None):
                    signonToken = self.token.getToken()
                    self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                reqItem.signinResponse(signonToken, data)
            else:
                signonToken = self.token.getToken()
                self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                reqItem.signinResponse(signonToken, data)
        else:
            logger.debug(f"signin failed for user {username}")
            reqItem.signinResponseFailed('invalid password')


    def signout(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        signonToken = parsedData["signon_token"]
        savedToken = self.db.getToken(username)
        if(savedToken == None):
            reqItem.signoutResponse('fail', 'currently not logged in')
            return

        self.db.logout(username)
        self.db.saveAccountInfo(username, parsedData)
        reqItem.signoutResponse("success")


    def getAccountInfo(self, parsedData):
        self.log_function_name()
        username = parsedData["username"]
        #signonToken = parsedData["signonToken"]
        data = self.db.getAccountInfo(username)
        return data
