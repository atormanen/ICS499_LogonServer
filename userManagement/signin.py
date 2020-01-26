from ICS499_LogonServer.database.mysqlDB import mysqlDB

class signin:
    mysqlDB = ''

    def __init__(self):
        self.mysqlDB = mysqlDB('admin','ICS4992020','localhost','userdb')

    def signin(parsedData):

		#mysqldb getPassword
        username = parsedData["username"]
        print("Inside signin")
		#compare password to given getPassword
        password = mysqlDB.getPasswordFor(username)
        print(password)
		#if signin succussful return true, else increment unssucsussful signin and
		#return False
