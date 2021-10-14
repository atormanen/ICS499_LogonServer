from global_logger import logger, VERBOSE
import inspect
import time


# Friends management will handle the mechanics of sending freinds reqeusts,
# handeling friends lists, and accepting fiend requests
class FriendsManagement:
    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, database):
        self.db = database

    def validateToken(self, username):
        self.log_function_name()
        tokenExpiration = self.db.getTokenCreationTime(username)
        token = self.db.getToken(username)
        if (token == None):
            return False
        currentTime = time.time()
        timeDiference = currentTime - tokenExpiration[0][0]
        if (timeDiference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True

    def validateUsername(self, username):
        self.log_function_name()
        if (self.db.validateUserExists(username)):
            return True
        return False

    def getFriendsList(self, parsed_data, reqItem):
        self.log_function_name()
        # connect to mysqldb to get FriendsList
        friendsList = self.db.getFriendsList(parsed_data["username"])
        reqItem.set_get_friends_list_response(friendsList)

    def getFriendRequests(self, parsed_data, reqItem):
        self.log_function_name()
        friendList = self.db.checkForFriendRequests(parsed_data["username"])
        reqItem.set_get_friend_requests_response(friendList)

    def getUserStats(self, username):
        self.log_function_name()
        if (self.validateUsername(username)):
            stats = self.db.getUserStats(username)
            return stats
        return False

    def sendFriendRequest(self, parsed_data, reqItem):
        self.log_function_name()
        # send a freind req
        username = parsed_data["username"]
        friendsUsername = parsed_data["friends_username"]

        if (self.validateUsername(username)):
            if (self.validateUsername(friendsUsername)):
                if (self.db.checkIfFriendRequestExists(username, friendsUsername) == 0):
                    # Friend request does not exists so go and make a request
                    result = self.db.sendFriendRequest(username, friendsUsername)
                    if (result == True):
                        reqItem.set_send_friend_request_response(was_successful=True)
                    else:
                        reqItem.set_send_friend_request_response(was_successful=False,
                                                                 failure_reason='The friend request does not exist.')
                else:
                    reqItem.set_send_friend_request_response(was_successful=False,
                                                             failure_reason="The friend's username is invalid.")
            else:
                reqItem.set_send_friend_request_response(was_successful=False,
                                                         failure_reason="The requester's request does not exist.")
                # reqItem.set_accept_friend_request_response(result)

    def accept_friend_request(self, parsed_data, reqItem):
        self.log_function_name()
        username = parsed_data["username"]
        friends_username = parsed_data["friends_username"]
        was_successful = False
        if self.validateUsername(username):
            if self.validateUsername(friends_username):
                was_successful = self.db.acceptFriendRequest(username, friends_username, True)
        reqItem.set_accept_friend_request_response(was_successful)

    def denyFriendRequest(self):
        self.log_function_name()
        return False

    def removeFriend(self, parsed_data, reqItem):
        self.log_function_name()
        username = parsed_data["username"]
        friends_username = parsed_data["friends_username"]

        if self.validateUsername(username) == False:
            reqItem.set_remove_friend_response(was_successful=False,
                                               failure_reason='username is not valid')
            return

        if not (self.validateToken(username)):
            reqItem.set_remove_friend_response(was_successful=False,
                                               failure_reason='invalid token')
            return

        if self.validateUsername(friends_username):
            result = self.db.removeFriend(username, friends_username)
            reqItem.set_remove_friend_response(was_successful=True)
        else:
            reqItem.set_remove_friend_response(was_successful=False,
                                               failure_reason='friends username not valid')
