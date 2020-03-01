#Is this class nececary? Should it be combined with signin?

class AccountManagement:
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.db = mysqlDB

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
