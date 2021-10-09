from userManagement.Signin import Signin
from userManagement.AccountManagement import AccountManagement
from userManagement.ValidateRequest import ValidateRequest
from database.DB import DB
from threading import Thread
from DataManagement.Responder import Responder
from DataManagement.MessageItem import MessageItem
import os
import json
from userManagement.FriendsManagement import FriendsManagement
from userManagement.Tokens import Tokens
from DataManagement.Leaderboard import Leaderboard
from Manifest import Manifest
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
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)
            return

        parsedData = reqItem.parsedData

        if parsedData["request_type"] == "signin":
            token = self.signin.signin(parsedData, reqItem)
            logger.debug(f"{reqItem.responseObj}")
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "createAccount":
            result = self.accountManager.createAccount(reqItem.parsedData)
            if result == True:
                reqItem.createAccountResponse('success')
            elif result == False:
                reqItem.createAccountResponse('fail')
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
        elif parsedData["request_type"] == "validateFriendRequest":
            #call friends management to validate friend request
            self.friendsManager.validateFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getFriendRequests":
            #call friends management to validate friend request
            self.friendsManager.getFriendRequests(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "removeFriend":
            self.friendsManager.removeFriend(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "signout":
            self.signin.signout(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getMostChessGamesWon":
            self.leaderboard.getMostChessGamesWon(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "getLongestWinStreak":
            self.leaderboard.getLongestWinStreak(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["request_type"] == "saveAccountInfoByKey":
            self.accountManager.saveAccountInfoByKey(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        # elif parsedData["request_type"] == "getAccountInfo":
        #    self.accountManager.getAccountInfo(parsedData)
        #    self.responder.sendResponse(reqItem)
        else:
            self.responder.sendBadRequest(reqItem.connectionSocket)


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
                logger.error('invalid request')
            finally:
                requestItem.invalidRequest()
                self.responder.sendResponse(requestItem)
