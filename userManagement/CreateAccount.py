#from database.MysqlDB import MysqlDB

class CreateAccount:
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def createAccount(self, parsedData):
		#check if username exists
        #return false if username alread exists
        self.checkUsernameAvailability(parsedData["username"])
        #call mysqlDB to create CreateAccount

        #if account createion succussful return true otherwise False
        return False

    def checkUsernameAvailability(self,username):
        self.mysqlDB.validateUsernameAvailable(username)
        return False
