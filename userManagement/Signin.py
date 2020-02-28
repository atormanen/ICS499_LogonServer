#Signin will handle the mechanics of signing a user in
class Signin:

    def __init__(self, db):
        self.db = db

    def validatePassword(self, username, password):
        dbPassword = self.db.getPasswordFor(username)
        dbPassword = dbPassword[0][0]
		#compare password to given getPassword
        if(password == dbPassword):
            return True
        return False

    def signin(self, parsedData):
        username = parsedData["username"]
        password = parsedData["password"]
        if(self.validatePassword(username, password)):
            #do the signin stuff
            #Generate a session token
            #Set a token expiration in the db
            #Bundle the tocken into the response package
            return True
        return False
