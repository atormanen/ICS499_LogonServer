#Is this class nececary? Should it be combined with signin?
from userManagement.Tokens import Tokens
import time
from global_logger import logger, VERBOSE

class AccountManagement:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.db = mysqlDB

    def validateUsername(self, username):
        self.log_function_name()
        if(self.db.validateUserExists(username)):
            return True
        return False

    def isPasswordValid(self, password):
        self.log_function_name()
        upper_ctr, lower_ctr, number_ctr, special_ctr = 0, 0, 0, 0
        for i in range(len(str)):
            if str[i] >= 'A' and str[i] <= 'Z': upper_ctr += 1
            elif str[i] >= 'a' and str[i] <= 'z': lower_ctr += 1
            elif str[i] >= '0' and str[i] <= '9': number_ctr += 1
            else: special_ctr += 1
        numberOfGoodChar = upper_ctr + number_ctr + special_ctr

        if(numberOfGoodChar >= 3):
            return True
        else:
            return False



    def createAccount(self, parsedData):
        self.log_function_name()
		#check if username exists
        #return false if username alread exists
        result = self.db.validateUsernameAvailable(parsedData["username"])

        #call mysqlDB to create CreateAccount
        if result == 0:
            self.db.createUser(parsedData)
            return True
        else:
            return False
        #if account createion succussful return true otherwise False

    def getUserStats(self, parsedData, reqItem):
        self.log_function_name()
        stats = self.db.getUserStats(parsedData["username"])
        reqItem.getUSerStatsResponse(stats[0])

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
            return False
        return True

    def changePassword(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        #signonToken = parsedData["signon_token"]
        oldPassword = parsedData["old_password"]
        newPassword = parsedData["new_password"]
        if(self.validatePassword(username, oldPassword)):
            # TODO remove commented out code if it is not needed
            # if(True):
                savedPassword = self.db.getPasswordFor(username)
                savedPassword = savedPassword[0][0]

                if(savedPassword == oldPassword):
                    self.db.changePassword(username, newPassword)
                    reqItem.changePasswordResponse("success")
                else:
                    reqItem.changePasswordResponse("fail")
            # else:
            #     print("token is not up to date")
            #     reqItem.changePasswordResponse("fail")
        else:
            reqItem.changePasswordResponse("fail")

    def saveAccountInfoByKey(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        signonToken = parsedData["signonToken"]
        hash = parsedData["hash"]
        key = parsedData["key"]
        value = parsedData["value"]
        type = parsedData["type"]
        if(self.validatePassword(username, hash)):
            self.db.saveAccountInfoByKey(username, key, value);
            reqItem.saveAccountInfoByKeyResponse("success")
        else:
            reqItem.saveAccountInfoByKeyResponse("fail")
