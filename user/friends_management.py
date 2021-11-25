import time

from data.message_item import GetFriendsListRequest, GetFriendRequestsRequest, SendFriendRequestRequest, \
    AcceptFriendRequestRequest, RemoveFriendRequest
from database.db import DB, FriendRequestNotFoundException, FailureException
from global_logger import logger


# Friends management will handle the mechanics of sending friends requests,
# handling friends lists, and accepting fiend requests
class FriendsManagement:

    def __init__(self, database: DB):
        self.db: DB = database

    # @logged_method
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

    # @logged_method
    def validate_username(self, username):
        if (self.db.user_exists(username)):
            return True
        return False

    # @logged_method
    def get_friends_list(self, req_item: GetFriendsListRequest):
        # connect to mysqldb to get FriendsList
        friends_list = self.db.get_friends_list(req_item.username)
        req_item.set_response(friends_list=friends_list)

    # @logged_method
    def get_friend_requests(self, req_item: GetFriendRequestsRequest):
        friend_list = self.db.check_for_friend_requests(req_item.username)
        req_item.set_response(friends_list=friend_list)

    # @logged_method
    def get_user_stats(self, username):
        if (self.validate_username(username)):
            stats = self.db.get_user_stats(username)
            return stats
        return False

    # @logged_method
    def send_friend_request(self, req_item: SendFriendRequestRequest):
        # send a friend req
        username = req_item.username
        friends_username = req_item.friends_username

        if (self.validate_username(username)):
            if (self.validate_username(friends_username)):
                if (not self.db.check_if_friend_request_exists(username, friends_username)):
                    # Friend request does not exists so go and make a request
                    result = self.db.send_friend_request(username, friends_username)
                    if (result is True):
                        req_item.set_response()
                    else:
                        req_item.set_response(failure_reason='The friend request does not exist.')
                else:
                    req_item.set_response(failure_reason="The friend's username is invalid.")
            else:
                req_item.set_response(failure_reason="The requester's request does not exist.")

    # @logged_method
    def accept_friend_request(self, req_item: AcceptFriendRequestRequest):
        username = req_item.username
        friends_username = req_item.friends_username
        if self.validate_username(username):
            if self.validate_username(friends_username):
                try:
                    self.db.accept_friend_request(username, friends_username, True)
                    req_item.set_response()
                except FriendRequestNotFoundException as e:
                    req_item.set_response(failure_reason=e.failure_reason_msg)

    # @logged_method
    def deny_friend_request(self):
        return False

    # @logged_method
    def remove_friend(self, req_item: RemoveFriendRequest):
        username = req_item.username
        friends_username = req_item.friends_username

        if not self.validate_username(username):
            req_item.set_response(failure_reason='username is not valid')
            return

        if not (self.validate_token(username)):
            req_item.set_response(failure_reason='invalid token')
            return

        if self.validate_username(friends_username):
            try:
                self.db.remove_friend(username, friends_username)
            except FailureException as e:
                req_item.set_response(failure_reason=e.failure_reason_msg)
        else:
            req_item.set_response(failure_reason='friends username not valid')
