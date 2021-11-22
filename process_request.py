import json

from data.leaderboard import Leaderboard
from data.message_item import BaseRequest
from data.responder import Responder
from data.test_message_item import REVOKE_FRIEND_REQUEST, GET_ACCOUNT_INFO, SAVE_ACCOUNT_INFO_BY_KEY, CHANGE_PASSWORD, \
    GET_MOST_CHESS_GAMES_WON, GET_LONGEST_WIN_STREAK, SIGNOUT, REMOVE_FRIEND, ACCEPT_FRIEND_REQUEST, \
    SEND_FRIEND_REQUEST, GET_FRIEND_REQUESTS, GET_FRIENDS_LIST, GET_USER_STATS, CREATE_ACCOUNT, SIGNIN
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
        with open('./params.json', 'r') as f:
            data = json.loads(f.read())
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
        self.responder = Responder(10.0)
        self.leaderboard = Leaderboard(self.database)

    # TODO: find a better way to process these requests types.
    @logged_method
    def process_request_type(self, req_item: BaseRequest):

        def _unimplemented(msg: str):
            # noinspection PyUnusedLocal
            def _callable(*args, **kwargs):
                raise NotImplementedError(msg)
            return _callable

        action_dict = {REVOKE_FRIEND_REQUEST: _unimplemented('revoke_friend_request has not been implemented yet'),
                       GET_ACCOUNT_INFO: _unimplemented('get_account_info has not been implemented yet'),
                       SAVE_ACCOUNT_INFO_BY_KEY: self.account_manager.save_account_info_by_key,
                       CHANGE_PASSWORD: self.account_manager.change_password,
                       GET_MOST_CHESS_GAMES_WON: self.leaderboard.get_most_chess_games_won,
                       GET_LONGEST_WIN_STREAK: self.leaderboard.get_longest_win_streak,
                       SIGNOUT: self.signin.signout,
                       REMOVE_FRIEND: self.friends_manager.remove_friend,
                       ACCEPT_FRIEND_REQUEST: self.friends_manager.accept_friend_request,
                       SEND_FRIEND_REQUEST: self.friends_manager.send_friend_request,
                       GET_FRIEND_REQUESTS: self.friends_manager.get_friend_requests,
                       GET_FRIENDS_LIST: self.friends_manager.get_friends_list,
                       GET_USER_STATS: self.account_manager.get_user_stats,
                       CREATE_ACCOUNT: self.account_manager.create_account,
                       SIGNIN: self.signin.signin}

        action_dict[req_item.request_type](req_item)

        self.responder.send_response(req_item.response, 10.0)

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
                self.responder.send_response(request_item, 10.0)
