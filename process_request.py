import json

from data.leaderboard import Leaderboard
from data.message_item import RequestType
from data.responder import Responder
from database.db import DB
from global_logger import logger, logged_method
from user.account_management import AccountManagement
from user.friends_management import FriendsManagement
from user.signin import Signin
from user.validate_request import RequestValidator


class ProcessRequest:

    # PrecessRequest is set up to be a separate process in the OS and
    # will hold the shared request queue object. It will pull requests
    # from the queue as they are inserted from the listener
    def __init__(self, request_queue):
        f = open('./params.json', 'r')
        data = json.loads(f.read())
        f.close()
        reader = data['db_host']
        writer = data['db_host']
        username = data['db_username']
        password = data['db_password']
        db_name = data['db_name']
        self.database = DB(username, password, reader, writer, db_name)
        # self.database = DB('app','123','192.168.1.106','db_name')

        self.request_queue = request_queue
        self.signin = Signin(self.database)
        self.account_manager = AccountManagement(self.database)
        self.friends_manager = FriendsManagement(self.database)
        self.req_validation = RequestValidator()
        self.responder = Responder()
        self.leaderboard = Leaderboard(self.database)

    # TODO: find a better way to process these requests types.
    @logged_method
    def process_request_type(self, req_item):
        if self.req_validation.is_bad_request(req_item.parsed_data):
            self.responder.send_bad_request(req_item.connection_socket)
            return

        parsed_data = req_item.parsed_data

        if parsed_data["request_type"] == RequestType.SIGNIN:
            token = self.signin.signin(parsed_data, req_item)
            logger.debug(f"{req_item.response_obj}")
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.CREATE_ACCOUNT:
            self.account_manager.create_account(req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.GET_USER_STATS:
            # call Account Management to get user stats
            self.account_manager.get_user_stats(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.CHANGE_PASSWORD:
            # call Account Management to get user stats
            self.account_manager.change_password(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.GET_FRIENDS_LIST:
            # call FriendsManager to retrieve friends list
            self.friends_manager.get_friends_list(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.SEND_FRIEND_REQUEST:
            # call FriendsManager to send friend request
            self.friends_manager.send_friend_request(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.ACCEPT_FRIEND_REQUEST:
            # call friends management to accept friend request
            self.friends_manager.accept_friend_request(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.GET_FRIEND_REQUESTS:
            # call friends management to get friend request
            self.friends_manager.get_friend_requests(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.REVOKE_FRIEND_REQUEST:
            # FIXME
            raise NotImplementedError('revoke_friend_request has not been implemented yet')
            self.friends_manager.get_friend_requests(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.REMOVE_FRIEND:
            self.friends_manager.remove_friend(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.SIGNOUT:
            self.signin.signout(parsed_data, req_item)
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.GET_MOST_CHESS_GAMES_WON:
            self.leaderboard.get_most_chess_games_won(req_item, parsed_data["number_of_games"])
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.GET_LONGEST_WIN_STREAK:
            self.leaderboard.get_longest_win_streak(req_item, parsed_data["number_of_games"])
            self.responder.send_response(req_item)
        elif parsed_data["request_type"] == RequestType.SAVE_ACCOUNT_INFO_BY_KEY:
            self.account_manager.save_account_info_by_key(parsed_data, req_item)
            self.responder.send_response(req_item)
        # elif parsed_data["request_type"] == "get_account_info":
        #    self.account_manager.get_account_info(parsed_data)
        #    self.responder.send_response(req_item)
        else:
            self.responder.send_bad_request(req_item.connection_socket)

    # The process thread will block on request_queue.get() until something
    # arrives.
    @logged_method
    def process_requests(self):

        while True:
            request_item = self.request_queue.get()
            # Decrypt parsed_data
            try:
                self.process_request_type(request_item)
            except Exception as e:
                logger.error(e)
                request_item.set_invalid_request_response()
                self.responder.send_response(request_item)
