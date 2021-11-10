import json

from data.leaderboard import Leaderboard
from data.message_item import BaseRequest
from data.responder import Responder
from data.test_message_item import REVOKE_FRIEND_REQUEST, GET_ACCOUNT_INFO, SAVE_ACCOUNT_INFO_BY_KEY, CHANGE_PASSWORD, \
    GET_MOST_CHESS_GAMES_WON, GET_LONGEST_WIN_STREAK, SIGNOUT, REMOVE_FRIEND, ACCEPT_FRIEND_REQUEST, \
    SEND_FRIEND_REQUEST, GET_FRIEND_REQUESTS, GET_FRIENDS_LIST, GET_USER_STATS, CREATE_ACCOUNT, SIGNIN
from database.db import DB, CouldNotConnectException
from global_logger import logger, logged_method
from user.account_management import AccountManagement
from user.friends_management import FriendsManagement
from user.signin import Signin
from user.validate_request import RequestValidator
from util.threading import ThreadController


class RequestProcessor:

    # PrecessRequest is set up to be a separate process in the OS and
    # will hold the shared request queue object. It will pull requests
    # from the queue as they are inserted from the listener
    def __init__(self, controller: ThreadController, request_queue, timeout_seconds: float):
        with open('./params.json', 'r') as f:
            data = json.loads(f.read())
        reader = data['db_host']
        writer = data['db_host']
        username = data['db_username']
        password = data['db_password']
        db_name = data['db_name']
        try:
            self.database = DB(username, password, reader, writer, db_name)
        except CouldNotConnectException as e:
            logger.error(e)
            raise RuntimeError("Startup failed due to inability to connect to db during initialization.") from e
        # self.database = DB('app','123','192.168.1.106','db_name')
        self.timeout_seconds = timeout_seconds
        self.request_queue = request_queue
        self.controller = controller
        self.signin = Signin(self.database)
        self.account_manager = AccountManagement(self.database)
        self.friends_manager = FriendsManagement(self.database)
        self.req_validation = RequestValidator()
        self.responder = Responder(timeout_seconds=timeout_seconds)
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

    # The process thread will block on request_queue.get() until something
    # arrives.
    @logged_method
    def process_requests(self):

        # we need to ensure that this will eventually recheck self.controller.should_stay_alive
        #   otherwise it could prevent the program from exiting properly. To do this we use a
        #   timeout value on any blocking calls that will wait.

        # We also want to anticipate potential issues like being unable to communicate with the client after processing
        #   the request. We can retry sending the response a number of times, before giving up and serving the next
        #   request.

        retry_send = False
        send_retry_count = 0
        max_send_retries = 5
        while self.controller.should_stay_alive:
            try:
                request_item = self.request_queue.get(timeout_seconds=self.timeout_seconds)
            except TimeoutError:
                continue
            # Decrypt parsed_data
            if request_item:
                if not retry_send:
                    # make response by processing the request
                    #   Note that we don't want this in a try.
                    #   We want any exceptions to be handled internally so that a appropriate response is ready to send.
                    self.process_request_type(request_item)

                # send response
                try:
                    self.responder.send_response(request_item, timeout_seconds=self.timeout_seconds)
                    retry_send = False
                    send_retry_count = 0
                except TimeoutError:
                    if send_retry_count < max_send_retries:
                        retry_send = True
                        send_retry_count += 1
                    else:
                        retry_send = False
                        send_retry_count = 0
