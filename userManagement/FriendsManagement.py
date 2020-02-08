#from database.MysqlDB import MysqlDB

class FriendsList:

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def getFriendsList(self, parsedData):
		#connect to mysqldb to get FriendsList
		return False


class SendFreindRequest:
    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def checkUserExists(self, username):
        #querry database if user exitsts
        return False

    def sendRequest(self, parsedData):
        #send request to client to be added as a frined

        #update friend in users db as a friend but keep req accepted as false

        return False

class ValidateFriendRequest:
    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def validateRequest(self, parsedData):
        #if request accepted, update as friend in db for BOTH User

        #if not eccepted, send response to requsetee, remove from # DEBUG:

        return False
