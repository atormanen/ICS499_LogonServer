#Friends management will handle the mechanics of sending freinds reqeusts,
#handeling friends lists, and accepting fiend requests
class FriendsManagement:

    def __init__(self, mysqlDB):
        self.mysqlDB = mysqlDB

    def getFriendsList(self, parsedData):
		#connect to mysqldb to get FriendsList
        #self.mysqlDB.getFriendsList(parsedData["username"])
	    return False

    def getUserStats(self):
        return False
