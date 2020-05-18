#Is this class nececary? Should it be combined with signin?
from userManagement.Tokens import Tokens
import time

class AccountManagement:
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.db = mysqlDB

    def validateUsername(self, username):
        if(self.db.validateUserExists(username)):
            return True
        return False

    def isPasswordValid(self, password):
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
        stats = self.db.getUserStats(parsedData["username"])
        reqItem.getUSerStatsResponse(stats[0])

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

    def changePassword(self, parsedData, reqItem):
        username = parsedData["username"]
        #signonToken = parsedData["signon_token"]
        oldPassword = parsedData["old_password"]
        newPassword = parsedData["new_password"]
        print(parsedData)
        if(self.validatePassword(username, oldPassword)):
            # TODO remove commented out code if it is not needed
            # if(True):
                savedPassword = self.db.getPasswordFor(username)
                savedPassword = savedPassword[0][0]
                print("saved password: " + str(savedPassword))
                print("new password: " + str(newPassword))

                if(savedPassword == oldPassword):
                    self.db.changePassword(username, newPassword)
                    reqItem.changePasswordResponse("success")
                else:
                    print("passwords do not match")
                    reqItem.changePasswordResponse("fail")
            # else:
            #     print("token is not up to date")
            #     reqItem.changePasswordResponse("fail")
        else:
            print("password validation failed")
            reqItem.changePasswordResponse("fail")

    def saveAccountInfo(self, parsedData, reqItem):
        username = parsedData["username"]
        signonToken = parsedData["signonToken"]
        hash = parsedData["hash"]
        key = parsedData["key"]
        value = parsedData["value"]
        type = parsedData["type"]
        if(self.validatePassword(username, hash)):
            self.db.saveAccountInfoByKey(username, key, value);
            reqItem.saveAccountInfoResponse("success")
        else:
            print("authentification failed")
            reqItem.saveAccountInfoResponse("fail")
