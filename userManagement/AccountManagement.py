#Is this class nececary? Should it be combined with signin?

class AccountManagement:
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.db = mysqlDB

    def validateUsername(self, username):
        if(self.db.validateUserExists(username)):
            return True
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
        signonToken = parsedData["signon_token"]
        oldPassword = parsedData["old_password"]
        newPassword = parsedData["new_password"]

        if(self.validatePassword(username, password)):
            if(self.tokenUpToDate(username)):
                savedPassword = self.db.getPassword(username)
                if(savedPassword == oldPassword):
                    self.db.changePassword(username, newPassword)
                    reqItem.changePasswordResponse("success")
                else:
                    reqItem.changePasswordResponse("fail")
            else:
                reqItem.changePasswordResponse("fail")
        else:
            reqItem.changePasswordResponse("fail")
