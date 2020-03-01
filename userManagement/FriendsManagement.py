#Friends management will handle the mechanics of sending freinds reqeusts,
#handeling friends lists, and accepting fiend requests
class FriendsManagement:

    def __init__(self, database):
        self.db = database

    def getFriendsList(self, parsedData, reqItem):
		#connect to mysqldb to get FriendsList
        friendsList = self.db.getFriendsList(parsedData["username"])
        reqItem.getFriendsListResponse(friendsList)

    def getUserStats(self, username):
        stats = self.db.getUserStats(username)
        return stats

    def sendFriendRequest(self, parsedData, reqItem):
        #send a freind req
        username = parsedData["username"]
        friendsUsername = parsedData["friendsUsername"]
        result = self.db.sendFriendRequest(username, friendsUsername)
        reqItem.sendFriendReqResponse(result)

    def validateFriendRequest(self, parsedData, reqItem):
        username = parsedData["username"]
        friendsUsername = parsedData["friendsUsername"]
        result = self.db.acceptFriendRequest(username, friendsUsername, True)
        reqItem.acceptFriendReqResponse(result)
