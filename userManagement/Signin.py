#from ..mysqlDB import mysqlDB
class Signin:

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def validatePassword(self, username, password):
        dbPassword = self.mysqlDB.getPasswordFor(username)
        dbPassword = dbPassword[0][0]
		#compare password to given getPassword
        if(password == dbPassword):
            return True
        return False

    def signin(self, parsedData):
        username = parsedData["username"]
        password = parsedData["password"]
        if(compareResult == self.validatePassword(username, password)):
            #do the signin stuff
        else:
            retrun False
