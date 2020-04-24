import json
#Message item is a wrapper class to hold the data of each reqeust.
#It holds the json object that was sent to the server as well as
#the socket

## TODO: Create subclasses for each message type.
#Too much happening here

class MessageItem:
    def __init__(self,connectionSocket, parsedData):
        self.connectionSocket = connectionSocket
        self.parsedData = parsedData
        self.responseObj = ''

    def signinResponse(self,token):
        response = {
                    "requestType":"signin",
                    "status":"success",
                    "token":""
        }
        response["token"] = token
        if not(token):
             response["status"] = "fail"
        self.responseObj = json.dumps(response)

    def createAccountResponse(self,status,reason='null'):
        response = {
                    "requestType":"createAccount",
                    "status":"",
                    "reason":""
        }
        response["status"] = status
        response["reason"] = reason
        self.responseObj = json.dumps(response)

    def getUSerStatsResponse(self, stats):
        response = {
                    "requestType":"getUserStats",
                    "userId":"",
                    "gamesPlayed":"",
                    "gamesWon":"",
                    "gamesResigned":"",
                    "score":"",
                    "longest_win_streak":""
        }
        response["userId"] = stats[0]
        response["gamesPlayed"] = stats[1]
        response["gamesWon"] = stats[2]
        response["gamesResigned"] = stats[3]
        response["score"] = stats[4]
        response["longest_win_streak"] = stats[5]
        self.responseObj = json.dumps(response)

    def getFriendsListResponse(self, friendsList):
        friendDict = {
                    "friend0":"friends"
        }

        i = 0
        for item in friendsList:
            user = {
                    "username":""
            }
            user["username"] = friendsList[0][1]

            friedStr = "friend" + str(i)
            friendDict[friedStr] = user
            i = i + 1
        response = {
                    "requestType":"getFriendsList",
                    "friends":""
        }
        response["friends"] = str(friendDict)
        self.responseObj = json.dumps(response)


    def acceptFriendReqResponse(self,status):
        response = {
                    "requestType":"validateFriendRequest",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def sendFriendReqResponse(self,status,reason='null'):
        response = {
                    "requestType":"sendFriendRequest",
                    "status":"",
                    "reason":""
        }
        response["status"] = status
        response["reason"] = reason
        self.responseObj = json.dumps(response)

    def signoutResponse(self, status):
        response = {
                    "requestType":"sendFriendRequest",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def longestWinStreakResponse(self, numberOfGames, data):
        response = {
                    "requestType":"getLongestWinStreak",
                    "numberOfGames":"",
                    "data":""
        }
        response["numberOfGames"] = numberOfGames
        response["data"] = data
        self.responseObj = json.dumps(response)

    def mostChessGamesWonResponse(self, numberOfGames, data):
        response = {
                    "requestType":"getMostChessGamesWon",
                    "numberOfGames":"",
                    "data":""
        }
        response["numberOfGames"] = numberOfGames
        response["data"] = str(data)
        self.responseObj = json.dumps(response)
