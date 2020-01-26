#from ..mysqlDB import mysqlDB
class Signin:
    test = ''
    mysqlDB = ''

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def signin(self, parsedData):

		#mysqldb getPassword
        username = parsedData["username"]
        print("Inside signin")
		#compare password to given getPassword
        password = self.mysqlDB.getPasswordFor(username)
        print(password)
		#if signin succussful return true, else increment unssucsussful signin and
		#return False
