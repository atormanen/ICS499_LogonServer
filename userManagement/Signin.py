#from ..mysqlDB import mysqlDB
class Signin:
    test = ''
    mysqlDB = ''

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def signin(self, parsedData):
        username = parsedData["username"]
        password = parsedData["password"]

		#get password from mysqldb
        password = self.mysqlDB.getPasswordFor(username)
		#compare password to given getPassword

		#if signin succussful return true, else increment unssucsussful signin and
		#return False

    def signinFailed(self):
        #connect to db and increment signin signinFailed
        return False
