#Validate request will check the initial variable to see what kind of request
#type it is.
## TODO: Check the entire json object for apropriate fields and not just the req type
class ValidateRequest:

    def __init__(self):
        self.num = 0

    def isBadRequest(self,parsedData):
        if parsedData["request_type"] == "signin":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsedData["request_type"] == "createAccount":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsedData["request_type"] == "changePassword":
            return False
        elif parsedData["request_type"] == "getUserStats":
            return False
        elif parsedData["request_type"] == "getFriendsList":
            return False
        elif parsedData["request_type"] == "sendFriendRequest":
            return False
        elif parsedData["request_type"] == "validateFriendRequest":
            return False
        elif parsedData["request_type"] == "signout":
            return False
        elif parsedData["request_type"] == "getMostChessGamesWon":
            return False
        elif parsedData["request_type"] == "removeFriend":
            return False
        elif parsedData["request_type"] == "getFriendRequests":
            return False
        elif parsedData["request_type"] == "getAccountInfo":
            return False
        elif parsedData["request_type"] == "saveAccountInfo":
            return False
        elif parsedData["request_type"] == "getLongestWinStreak":
            return False
        elif parsedData["request_type"] == "saveAccountInfoByKey":
            return False
        else:
            #self.requestQueue.put(RequestItem(connectionSocket,parsedData))
            return True
