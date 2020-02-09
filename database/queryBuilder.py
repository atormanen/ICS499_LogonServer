import time
import json
class queryBuilder:
    tableName = ''

    def __init__(self):
        self.tableName = 'test'

    def buildQuery(self, data):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        parsedData = json.loads(data)
        return insertStatement

    def getPasswordFor(self, username):
        selectStatement = "SELECT password from player where username ='" +\
            username + "'"
        return selectStatement

    def validateUserExists(self,username):
        return "SELECT EXISTS(SLECT username FROM user WHERE username = " +\
            username + " );"

    def validateUsernameAvailable(self,username):
        return "SELECT EXISTS(SELECT username FROM user WHERE username = '" +\
            username + "' );"

    def getLastUserId(self):
        return "SELECT MAX(user_id) FROM user;"

    def createUser(self, id, parsedData):
        return "INSERT INTO user VALUES("+ id +",'" + parsedData["username"] +\
            "','" +parsedData["firstName"] + "','" + parsedData["lastName"] +\
            "','" + parsedData["email"] + "',0,'" + parsedData["password"] +\
             "');"

    def createUserStats(self, id):
        return "INSERT INTO user_statistics VALUES("+ id +" ,0,0,0,0,0,1);"
