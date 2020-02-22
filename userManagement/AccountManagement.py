#from database.MysqlDB import MysqlDB

class AccountManagement:
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def createAccount(self, parsedData):
		#check if username exists
        #return false if username alread exists
        result = self.mysqlDB.validateUsernameAvailable(parsedData["username"])
        #call mysqlDB to create CreateAccount
        if result == 0:
            self.mysqlDB.createUser(parsedData)
            return True
        else:
            return False
        #if account createion succussful return true otherwise False
