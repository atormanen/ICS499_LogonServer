#from database.MysqlDB import MysqlDB

class CreateAccount:
    mysqlDB = ''
    test = ''
    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def createAccount(self, parsedData):
		#mysqldb getPassword
        print("Inside createAccount")
		#compare password to given getPassword

		#if signin succussful return true, else increment unssucsussful signin and
		#return False
