from database.mysqlDB import mysqlDB

class createAccount:
    mysqlDB = ''
    username = ""
    password = ""

    def __init__(self):
        self.mysqlDB = mysqlDB('admin','ICS4992020','localhost','userdb')

    def createAccount(parsedData):
		#mysqldb getPassword
        print("Inside createAccount")
		#compare password to given getPassword

		#if signin succussful return true, else increment unssucsussful signin and
		#return False
