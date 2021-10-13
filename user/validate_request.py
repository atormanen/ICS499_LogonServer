from global_logger import logger, VERBOSE
import inspect

#Validate request will check the initial variable to see what kind of request
#type it is.
## TODO: Check the entire json object for apropriate fields and not just the req type
class ValidateRequest:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self):
        self.num = 0

    def isBadRequest(self,parsed_data):
        self.log_function_name()
        if parsed_data["request_type"] == "signin":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsed_data["request_type"] == "createAccount":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsed_data["request_type"] == "changePassword":
            return False
        elif parsed_data["request_type"] == "getUserStats":
            return False
        elif parsed_data["request_type"] == "getFriendsList":
            return False
        elif parsed_data["request_type"] == "sendFriendRequest":
            return False
        elif parsed_data["request_type"] == "accept_friend_request":
            return False
        elif parsed_data["request_type"] == "signout":
            return False
        elif parsed_data["request_type"] == "get_most_chess_games_won":
            return False
        elif parsed_data["request_type"] == "removeFriend":
            return False
        elif parsed_data["request_type"] == "getFriendRequests":
            return False
        elif parsed_data["request_type"] == "getAccountInfo":
            return False
        elif parsed_data["request_type"] == "saveAccountInfo":
            return False
        elif parsed_data["request_type"] == "get_longest_win_streak":
            return False
        elif parsed_data["request_type"] == "saveAccountInfoByKey":
            return False
        elif parsed_data["requestType"] == "saveAccountInfoByKey":
            return False
        else:
            #self.requestQueue.put(RequestItem(connectionSocket,parsed_data))
            return True
