import time

from database.db import DB
from global_logger import logger, logged_method


# Friends management will handle the mechanics of sending friends requests,
# handling friends lists, and accepting fiend requests
class FriendsManagement:

    def __init__(self, database: DB):
        self.db: DB = database

    @logged_method
    def validate_token(self, username):
        token_expiration = self.db.get_token_creation_time(username)
        token = self.db.get_token(username)
        if (token is None):
            return False
        current_time = time.time()
        time_difference = current_time - token_expiration[0][0]
        if (time_difference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True

    @logged_method
    def validate_username(self, username):
        if (self.db.validate_user_exists(username)):
            return True
        return False

    @logged_method
    def get_friends_list(self, parsed_data, req_item):
        # connect to mysqldb to get FriendsList
        friends_list = self.db.get_friends_list(parsed_data["username"])
        req_item.set_get_friends_list_response(friends_list)

    @logged_method
    def get_friend_requests(self, parsed_data, req_item):
        friend_list = self.db.check_for_friend_requests(parsed_data["username"])
        req_item.set_get_friend_requests_response(friend_list)

    @logged_method
    def get_user_stats(self, username):
        if (self.validate_username(username)):
            stats = self.db.get_user_stats(username)
            return stats
        return False

    @logged_method
    def send_friend_request(self, parsed_data, req_item):
        # send a friend req
        username = parsed_data["username"]
        friends_username = parsed_data["friends_username"]

        if (self.validate_username(username)):
            if (self.validate_username(friends_username)):
                if (self.db.check_if_friend_request_exists(username, friends_username) == 0):
                    # Friend request does not exists so go and make a request
                    result = self.db.send_friend_request(username, friends_username)
                    if (result is True):
                        req_item.set_send_friend_request_response(was_successful=True)
                    else:
                        req_item.set_send_friend_request_response(was_successful=False,
                                                                  failure_reason='The friend request does not exist.')
                else:
                    req_item.set_send_friend_request_response(was_successful=False,
                                                              failure_reason="The friend's username is invalid.")
            else:
                req_item.set_send_friend_request_response(was_successful=False,
                                                          failure_reason="The requester's request does not exist.")
                # req_item.set_accept_friend_request_response(result)

    @logged_method
    def accept_friend_request(self, parsed_data, req_item):
        username = parsed_data["username"]
        friends_username = parsed_data["friends_username"]
        was_successful = False
        if self.validate_username(username):
            if self.validate_username(friends_username):
                was_successful = self.db.accept_friend_request(username, friends_username, True)
        req_item.set_accept_friend_request_response(was_successful)

    @logged_method
    def deny_friend_request(self):
        return False

    @logged_method
    def remove_friend(self, parsed_data, req_item):
        username = parsed_data["username"]
        friends_username = parsed_data["friends_username"]

        if not self.validate_username(username):
            req_item.set_remove_friend_response(was_successful=False,
                                                failure_reason='username is not valid')
            return

        if not (self.validate_token(username)):
            req_item.set_remove_friend_response(was_successful=False,
                                                failure_reason='invalid token')
            return

        if self.validate_username(friends_username):
            result = self.db.remove_friend(username, friends_username)
            req_item.set_remove_friend_response(was_successful=True)
        else:
            req_item.set_remove_friend_response(was_successful=False,
                                                failure_reason='friends username not valid')
