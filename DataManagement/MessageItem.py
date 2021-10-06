import json
from global_logger import logger, VERBOSE
import inspect
#Message item is a wrapper class to hold the data of each reqeust.
#It holds the json object that was sent to the server as well as
#the socket

## TODO: Create subclasses for each message type.
#Too much happening here

class MessageItem:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self,connectionSocket, parsedData):
        self.connectionSocket = connectionSocket
        self.parsedData = parsedData
        self.responseObj = ''

    def signinResponse(self,token, data):
        self.log_function_name()
        response = {
                    "request_type":"signin",
                    "status":"success",
                    "token":"",
                    "avatar_style":"",
                    "chessboard_style":"",
                    "chesspiece_style":"",
                    "match_clock_choice":"",
                    "automatic_queening":"",
                    "disable_pausing":"",
                    "require_commit_press":"",
                    "level":""
        }
        if not(token):
            response["status"] = "fail"
            self.responseObj = json.dumps(response)
        logger.debug(data)
        response["token"] = token
        response["avatar_style"] = data[0][0]
        response["chessboard_style"] = data[0][1]
        response["chesspiece_style"] = data[0][2]
        response["match_clock_choice"] = data[0][3]
        response["automatic_queening"] = data[0][4]
        response["disable_pausing"] = data[0][5]
        response["require_commit_press"] = data[0][6]
        response["level"] = data[0][7]
        self.responseObj = json.dumps(response)


    def createAccountResponse(self,status,reason='null'):
        self.log_function_name()
        response = {
                    "request_type":"createAccount",
                    "status":"",
                    "reason":""
        }
        response["status"] = status
        response["reason"] = reason
        self.responseObj = json.dumps(response)

    def getUSerStatsResponse(self, stats):
        self.log_function_name()
        response = {
                    "request_type":"getUserStats",
                    "user_id":"",
                    "games_played":"",
                    "games_won":"",
                    "games_resigned":"",
                    "score":"",
                    "longest_win_streak":""
        }
        response["user_id"] = stats[0]
        response["games_played"] = stats[1]
        response["games_won"] = stats[2]
        response["games_resigned"] = stats[3]
        response["score"] = stats[4]
        response["longest_win_streak"] = stats[5]
        self.responseObj = json.dumps(response)

    def getFriendsListResponse(self, friendsList, request = "getFriendsList"):
        self.log_function_name()
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
                    "request_type":"getFriendsList",
                    "count":"",
                    "friends":""
        }
        response["request_type"] = request
        response["count"] = len(friendsList)
        response["friends"] = str(friendDict)
        self.responseObj = json.dumps(response)



    def getFriendRequestsResp(self, friendsList):
        self.log_function_name()
        self.getFriendsListResponse(friendsList, "getFriendRequests")


    def acceptFriendReqResponse(self,status):
        self.log_function_name()
        response = {
                    "request_type":"validateFriendRequest",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def sendFriendReqResponse(self,status,reason='null'):
        self.log_function_name()
        response = {
                    "request_type":"sendFriendRequest",
                    "status":"",
                    "reason":""
        }
        response["status"] = status
        response["reason"] = reason
        self.responseObj = json.dumps(response)

    def removeFriendResponse(self, status):
        self.log_function_name()
        response = {
                    "request_type":"removeFriend",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)


    def signoutResponse(self, status):
        self.log_function_name()
        response = {
                    "request_type":"signout",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def longestWinStreakResponse(self, numberOfGames, data):
        self.log_function_name()
        response = {
                    "request_type":"getLongestWinStreak",
                    "number_of_games":"",
                    "data":""
        }
        response["number_of_games"] = numberOfGames
        response["data"] = data
        self.responseObj = json.dumps(response)

    def mostChessGamesWonResponse(self, numberOfGames, data):
        self.log_function_name()
        response = {
                    "request_type":"getMostChessGamesWon",
                    "number_of_games":"",
                    "data":""
        }
        response["number_of_games"] = numberOfGames
        response["data"] = str(data)
        self.responseObj = json.dumps(response)

    def changePasswordResponse(self, status):
        self.log_function_name()
        response = {
                    "request_type":"changePassword",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def saveAccountInfoByKeyResponse(self, status):
        self.log_function_name()
        response = {
                    "request_type":"saveAccountInfoByKey",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def saveAccountInfoByKeyResponse(self, status):
        self.log_function_name()
        response = {
                    "request_type":"saveAccountInfoByKey",
                    "status":""
        }
        response["status"] = status
        self.responseObj = json.dumps(response)

    def getAccountInfoResponse(self, data):
        self.log_function_name()
        response = {
                    "request_type":"getAccountInfo",
                    "avatar_style":"",
                    "chessboard_style":"",
                    "chesspiece_style":"",
                    "match_clock_choice":"",
                    "automatic_queening":"",
                    "disable_pausing":"",
                    "require_commit_press":"",
                    "level":""

        }
        response["avatar_style"] = data[0][0]
        response["chessboard_style"] = data[0][1]
        response["chesspiece_style"] = data[0][2]
        response["match_clock_choice"] = data[0][3]
        response["automatic_queening"] = data[0][4]
        response["disable_pausing"] = data[0][5]
        response["require_commit_press"] = data[0][6]
        response["level"] = data[0][7]
        self.responseObj = json.dumps(response)
