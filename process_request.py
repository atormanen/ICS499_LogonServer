from user.signin import Signin
from user.account_management import AccountManagement
from user.validate_request import RequestValidator
from database.db import DB
from threading import Thread
from data.responder import Responder
from data.message_item import MessageItem
import os
import json
from user.friends_management import FriendsManagement
from user.tokens import Tokens
from data.leaderboard import Leaderboard
from manifest import Manifest
from global_logger import logger, VERBOSE
from data.message_item import RequestType
import inspect

class ProcessRequest:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    #PrecessReqeust is set up to be a seperate process in the OS and
    #will hold the shared request queue object. It will pull requests
    #from the queue as they are inserted from the listener
    def __init__(self, requestQueue):
        f = open('./params.json','r')
        data = json.loads(f.read())
        f.close()
        reader = data['db_host']
        writer = data['db_host']
        username = data['db_username']
        password = data['db_password']
        db_name = data['db_name']
        self.database = DB(username, password, reader, writer, db_name)
        #self.database = DB('app','123','192.168.1.106','userdb')
        self.requestQueue = requestQueue
        self.signin = Signin(self.database)
        self.accountManager = AccountManagement(self.database)
        self.friendsManager = FriendsManagement(self.database)
        self.reqValidation = RequestValidator()
        self.responder = Responder()
        self.leaderboard = Leaderboard(self.database)

    ## TODO: find a better way to process these requests types.
    def proccesRequestType(self, reqItem):
        self.log_function_name()
        if self.reqValidation.is_bad_request(reqItem.parsed_data):
            self.responder.sendBadRequest(reqItem.connection_socket)
            return

        parsed_data = reqItem.parsed_data

        if parsed_data["request_type"] == RequestType.SIGNIN:
            token = self.signin.signin(parsed_data, reqItem)
            logger.debug(f"{reqItem.response_obj}")
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.CREATE_ACCOUNT:
            self.accountManager.createAccount(reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.GET_USER_STATS:
            #call Account Management to get user stats
            self.accountManager.getUserStats(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.CHANGE_PASSWORD:
            #call Account Management to get user stats
            self.accountManager.changePassword(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.GET_FRIENDS_LIST:
            #call FriendsManager to retrieve friends list
            self.friendsManager.getFriendsList(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.SEND_FRIEND_REQUEST:
            #call FriendsManager to send friend request
            self.friendsManager.sendFriendRequest(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.ACCEPT_FRIEND_REQUEST:
            #call friends management to accept friend request
            self.friendsManager.accept_friend_request(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.GET_FRIEND_REQUESTS:
            #call friends management to get friend request
            self.friendsManager.getFriendRequests(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.REVOKE_FRIEND_REQUEST:
            # FIXME
            raise NotImplementedError('revokeFriendRequest has not been implemented yet')
            self.friendsManager.getFriendRequests(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.REMOVE_FRIEND:
            self.friendsManager.removeFriend(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.SIGNOUT:
            self.signin.signout(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.GET_MOST_CHESS_GAMES_WON:
            self.leaderboard.get_most_chess_games_won(reqItem, parsed_data["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.GET_LONGEST_WIN_STREAK:
            self.leaderboard.get_longest_win_streak(reqItem, parsed_data["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsed_data["request_type"] == RequestType.SAVE_ACCOUNT_INFO_BY_KEY:
            self.accountManager.saveAccountInfoByKey(parsed_data, reqItem)
            self.responder.sendResponse(reqItem)
        # elif parsed_data["request_type"] == "getAccountInfo":
        #    self.accountManager.getAccountInfo(parsed_data)
        #    self.responder.sendResponse(reqItem)
        else:
            self.responder.sendBadRequest(reqItem.connection_socket)


    #The process thread will block on requestQueue.get() until something
    #arrives.
    def processRequests(self):
        self.log_function_name()
        while True:
            requestItem = self.requestQueue.get()
            #Decrypt parsed_data
            try:
                self.proccesRequestType(requestItem)
            except Exception as e:
                logger.error(e)
                requestItem.set_invalid_request_response()
                self.responder.sendResponse(requestItem)
