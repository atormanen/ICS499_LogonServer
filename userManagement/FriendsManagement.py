from global_logger import logger, VERBOSE
import inspect
import time

#Friends management will handle the mechanics of sending freinds reqeusts,
#handeling friends lists, and accepting fiend requests
class FriendsManagement:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, database):
        self.db = database


    def validateToken(self,username):
        self.log_function_name()
        tokenExpiration = self.db.getTokenCreationTime(username)
        token = self.db.getToken(username)
        if(token == None):
            return False
        currentTime = time.time()
        timeDiference = currentTime - tokenExpiration[0][0]
        if(timeDiference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True


    def validateUsername(self, username):
        self.log_function_name()
        if(self.db.validateUserExists(username)):
            return True
        return False

    def getFriendsList(self, parsedData, reqItem):
        self.log_function_name()
		#connect to mysqldb to get FriendsList
        friendsList = self.db.getFriendsList(parsedData["username"])
        reqItem.getFriendsListResponse(friendsList)

    def getFriendRequests(self, parsedData, reqItem):
        self.log_function_name()
        friendList = self.db.checkForFriendRequests(parsedData["username"])
        reqItem.getFriendRequestsResp(friendList)

    def getUserStats(self, username):
        self.log_function_name()
        if(self.validateUsername(username)):
            stats = self.db.getUserStats(username)
            return stats
        return False

    def sendFriendRequest(self, parsedData, reqItem):
        self.log_function_name()
        #send a freind req
        username = parsedData["username"]
        friendsUsername = parsedData["friends_username"]

        if(self.validateUsername(username)):
            if(self.validateUsername(friendsUsername)):
                if(self.db.checkIfFriendRequestExists(username, friendsUsername) == 0):
                    #Friend request does not exists so go and make a request
                    result = self.db.sendFriendRequest(username, friendsUsername)
                    if(result == True):
                        reqItem.sendFriendReqResponse("success")
                    else:
                        reqItem.sendFriendReqResponse("fail")
                else:
                    reqItem.sendFriendReqResponse("fail")
            else:
                reqItem.sendFriendReqResponse("fail")
        #reqItem.acceptFriendReqResponse(result)


    def validateFriendRequest(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        friendsUsername = parsedData["friends_username"]
        result = 'fail'

        friendList = self.db.checkForFriendRequests(parsedData["username"])

        if(len(friendList) == 0):
            reqItem.acceptFriendReqResponse('fail', 'friend is not friend request list')
            return

        friend_in_list = False
        for friend in friendList:
            if(friend[1] == friendsUsername):
                friend_in_list = True
                break

        if not(friend_in_list):
            reqItem.acceptFriendReqResponse('fail', 'friend is not in friend request list')
            return

        if(self.validateUsername(username)):
            if(self.validateUsername(friendsUsername)):
                self.db.acceptFriendRequest(username, friendsUsername, True)
                result = 'success'
        reqItem.acceptFriendReqResponse(result)


    def denyFriendRequest(self):
        self.log_function_name()
        return False

    def removeFriend(self, parsedData, reqItem):
        self.log_function_name()
        username = parsedData["username"]
        friendsUsername = parsedData["friends_username"]

        if(self.validateUsername(username) == False):
            reqItem.removeFriendResponse('fail','username is not valid')
            return

        if not(self.validateToken(username)):
            reqItem.removeFriendResponse('fail', 'invalid token')
            return

        if(self.validateUsername(friendsUsername)):
            result = self.db.removeFriend(username, friendsUsername)
            reqItem.removeFriendResponse("success")
        else:
            reqItem.removeFriendResponse("fail", 'friends username not valid')
