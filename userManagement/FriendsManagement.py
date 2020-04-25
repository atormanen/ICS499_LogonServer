#Friends management will handle the mechanics of sending freinds reqeusts,
#handeling friends lists, and accepting fiend requests
class FriendsManagement:

    def __init__(self, database):
        self.db = database

    def validateUsername(self, username):
        if(self.db.validateUserExists(username)):
            return True
        return False

    def getFriendsList(self, parsedData, reqItem):
		#connect to mysqldb to get FriendsList
        friendsList = self.db.getFriendsList(parsedData["username"])
        reqItem.getFriendsListResponse(friendsList)

    def getFreindRequestResp(self, parsedData, reqItem):
        friendList = self.db.checkForFriendRequests(parsedData["username"])
        print("friendList: " + friendList)
        reqItem.getFriendRequestsResp(friendList)

    def getUserStats(self, username):
        if(self.validateUsername(username)):
            stats = self.db.getUserStats(username)
            return stats
        return False

    def sendFriendRequest(self, parsedData, reqItem):
        #send a freind req
        username = parsedData["username"]
        friendsUsername = parsedData["friendsUsername"]

        if(self.validateUsername(username)):
            if(self.validateUsername(friendsUsername)):
                result = self.db.sendFriendRequest(username, friendsUsername)
                if(result == True):
                    reqItem.sendFriendReqResponse("success")
                else:
                    reqItem.sendFriendReqResponse("fail")
            else:
                reqItem.sendFriendReqResponse("fail")
        #reqItem.acceptFriendReqResponse(result)

    def validateFriendRequest(self, parsedData, reqItem):
        username = parsedData["username"]
        friendsUsername = parsedData["friendsUsername"]
        result = False
        if(self.validateUsername(username)):
            if(self.validateUsername(friendsUsername)):
                result = self.db.acceptFriendRequest(username, friendsUsername, True)
        reqItem.acceptFriendReqResponse(result)


    def denyFriendRequest(self):

        return False

    def removeFriend(self, parsedData, reqItem):
        username = parsedData["username"]
        friendsUsername = parsedData["friendsUsername"]
        if(self.validateUsername(friendsUsername)):
            result = self.db.removeFriend(username, friendsUsername)
            reqItem.removeFriendResponse("success")
        else:
            reqItem.removeFriendResponse("fail")
