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
        elif parsedData["requestType"] == "getUserStats":
            return False
        elif parsedData["requestType"] == "getFriendsList":
            return False
        elif parsedData["requestType"] == "sendFriendRequest":
            return False
        elif parsedData["requestType"] == "validateFriendRequest":
            return False
        else:
            #self.requestQueue.put(RequestItem(connectionSocket,parsedData))
            return True
