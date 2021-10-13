from global_logger import logger, VERBOSE
import inspect

# Signin will handle the mechanics of signing a user in
from user.tokens import Tokens
import time


class Signin:
    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, db):
        self.db = db
        self.token = Tokens()

    def validatePassword(self, username, password):
        self.log_function_name()
        if (self.db.validateUserExists(username)):
            dbPassword = self.db.getPasswordFor(username)
            dbPassword = dbPassword[0][0]
            # compare password to given getPassword
            if (password == dbPassword):
                return True
        return False

    def tokenUpToDate(self, username):
        self.log_function_name()
        tokenExpiration = self.db.getTokenCreationTime(username)
        # if(tokenExpiration):
        #    return False
        currentTime = time.time()
        timeDiference = currentTime - tokenExpiration[0][0]
        if (timeDiference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True

    def signin(self, parsed_data, reqItem):
        self.log_function_name()
        username = parsed_data["username"]
        password = parsed_data["password"]
        data = self.getAccountInfo(parsed_data)

        if (self.validatePassword(username, password)):
            if (self.tokenUpToDate(username)):
                # Bundle the tocken into the response package
                signonToken = self.db.getToken(username)
                signonToken = signonToken[0][0]
                logger.debug(type(signonToken))
                if (signonToken == None):
                    signonToken = self.token.getToken()
                    self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                reqItem.set_signin_response(signonToken, data)
            else:
                signonToken = self.token.getToken()
                self.db.signin(username, signonToken, self.token.getTokenCreationTime())
                reqItem.set_signin_response(signonToken, data)
        else:
            logger.debug(f"signin failed for user {username}")
            reqItem.set_signin_response_failed('invalid password')

    def signout(self, parsed_data, req_item):
        self.log_function_name()
        username = parsed_data["username"]
        signon_token = parsed_data["signon_token"]
        saved_token = self.db.getToken(username)
        saved_token = saved_token[0][0]
        if saved_token == None:
            req_item.set_signout_response(was_successful=False,
                                          failure_reason='currently not logged in')
            return

        self.db.logout(username)
        self.db.saveAccountInfo(username, parsed_data)
        req_item.set_signout_response(was_successful=True)

    def getAccountInfo(self, parsed_data):
        self.log_function_name()
        username = parsed_data["username"]
        # signonToken = parsed_data["signonToken"]
        data = self.db.getAccountInfo(username)
        return data
