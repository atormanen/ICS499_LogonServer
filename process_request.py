from user.signin import Signin
from user.account_management import AccountManagement
from user.validate_request import ValidateRequest
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
        self.reqValidation = ValidateRequest()
        self.responder = Responder()
        self.leaderboard = Leaderboard(self.database)

    ## TODO: find a better way to process these requests types.
    def proccesRequestType(self, reqItem):
        self.log_function_name()
        if self.reqValidation.isBadRequest(reqItem.parsed_data):
            self.responder.sendBadRequest(reqItem.connection_socket)
            return

        parsedData = reqItem.parsed_data

        if parsedData["request_type"] == "signin":
            token = self.signin.signin(parsedData, reqItem)
            logger.debug(f"{reqItem.response_obj}")
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "createAccount":
            self.accountManager.createAccount(reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getUserStats":
            #call Account Management to get user stats
            self.accountManager.getUserStats(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "changePassword":
            #call Account Management to get user stats
            self.accountManager.changePassword(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getFriendsList":
            #call FriendsManager to retrieve friends list
            self.friendsManager.getFriendsList(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "sendFriendRequest":
            #call FriendsManager to send friend request
            self.friendsManager.sendFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "accept_friend_request":
            #call friends management to validate friend request
            self.friendsManager.accept_friend_request(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getFriendRequests":
            #call friends management to validate friend request
            self.friendsManager.getFriendRequests(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "revokeFriendRequest":
            # FIXME
            raise NotImplementedError('revokeFriendRequest has not been implemented yet')
            self.friendsManager.getFriendRequests(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "removeFriend":
            self.friendsManager.removeFriend(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "signout":
            self.signin.signout(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "get_most_chess_games_won":
            self.leaderboard.get_most_chess_games_won(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "get_longest_win_streak":
            self.leaderboard.get_longest_win_streak(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "saveAccountInfoByKey":
            self.accountManager.saveAccountInfoByKey(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        # elif parsedData["request_type"] == "getAccountInfo":
        #    self.accountManager.getAccountInfo(parsedData)
        #    self.responder.sendResponse(reqItem)
        else:
            self.responder.sendBadRequest(reqItem.connection_socket)


    #The process thread will block on requestQueue.get() until something
    #arrives.
    def processRequests(self):
        self.log_function_name()
        while True:
            requestItem = self.requestQueue.get()
            #Decrypt parsedData
            try:
                self.proccesRequestType(requestItem)
            except Exception as e:
                logger.error(e)
                requestItem.set_invalid_request_response()
                self.responder.sendResponse(requestItem)
