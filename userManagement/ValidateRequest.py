#Validate request will check the initial variable to see what kind of request
#type it is.
## TODO: Check the entire json object for apropriate fields and not just the req type
class ValidateRequest:

    def __init__(self):
        self.num = 0

    def isBadRequest(self,parsedData):
        if parsedData["requestType"] == "signin":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsedData["requestType"] == "createAccount":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsedData["requestType"] == "changePassword":
            return False
        elif parsedData["requestType"] == "getUserStats":
            return False
        elif parsedData["requestType"] == "getFriendsList":
            return False
        elif parsedData["requestType"] == "sendFriendRequest":
            return False
        elif parsedData["requestType"] == "validateFriendRequest":
            return False
        elif parsedData["requestType"] == "signout":
            return False
        elif parsedData["requestType"] == "getMostChessGamesWon":
            return False
        elif parsedData["requestType"] == "removeFriend":
            return False
        elif parsedData["requestType"] == "getFriendRequests":
            return False
        elif parsedData["requestType"] == "getAccountInfo":
            return False
        elif parsedData["requestType"] == "saveAccountInfo":
            return False
        elif parsedData["requestType"] == "getLongestWinStreak":
            return False
        else:
            #self.requestQueue.put(RequestItem(connectionSocket,parsedData))
            return True
