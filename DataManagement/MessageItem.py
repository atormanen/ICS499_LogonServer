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

    def signinResponse(self,token, data):
        response = {
                    "requestType":"signin",
                    "status":"success",
                    "token":"",
                    "avatarStyle":"",
                    "chessboardStyle":"",
                    "chesspieceStyle":"",
                    "matchClockChoice":"",
                    "automaticQueening":"",
                    "disablePausing":"",
                    "requireCommitPress":"",
                    "level":""
        }
        if not(token):
            response["status"] = "fail"
            self.responseObj = json.dumps(response)
        response["token"] = token
        response["avatarStyle"] = data[0][0]
        response["chessboardStyle"] = data[0][1]
        response["chesspieceStyle"] = data[0][2]
        response["matchClockChoice"] = data[0][3]
        response["automaticQueening"] = data[0][4]
        response["disablePausing"] = data[0][5]
        response["requireCommitPress"] = data[0][6]
        response["level"] = data[0][7]
        print(response)
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

    def getFriendsListResponse(self, friendsList, request = "getFriendsList"):
        friendDict = {
                    "friend0":"friends"
        }

        i = 0
        for item in friendsList:
            user = {
                    "username":""
            }
            user["username"] = item[1]

            friedStr = "friend" + str(i)
            friendDict[friedStr] = user
            i = i + 1
        response = {
                    "requestType":"getFriendsList",
                    "count":"",
                    "friends":""
        }
        response["requestType"] = request
        response["count"] = len(friendsList)
        response["friends"] = str(friendDict)
        self.responseObj = json.dumps(response)



    def getFriendRequestsResp(self, friendsList):
        self.getFriendsListResponse(friendsList, "getFriendRequests")


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

    def removeFriendResponse(self, status):
        response = {
                    "requestType":"removeFriend",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)


    def signoutResponse(self, status):
        response = {
                    "requestType":"signout",
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

    def changePasswordResponse(self, status):
        response = {
                    "requestType":"changePassword",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def getAccountInfoResponse(self, data):
        response = {
                    "requestType":"getAccountInfo",
                    "avatarStyle":"",
                    "chessboardStyle":"",
                    "chesspieceStyle":"",
                    "matchClockChoice":"",
                    "automaticQueening":"",
                    "disablePausing":"",
                    "requireCommitPress":"",
                    "level":""

        }
        response["avatarStyle"] = data[0][0]
        response["chessboardStyle"] = data[0][1]
        response["chesspieceStyle"] = data[0][2]
        response["matchClockChoice"] = data[0][3]
        response["automaticQueening"] = data[0][4]
        response["disablePausing"] = data[0][5]
        response["requireCommitPress"] = data[0][6]
        response["level"] = data[0][7]
        self.responseObj = json.dumps(response)
