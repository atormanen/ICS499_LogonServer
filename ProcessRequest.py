from userManagement.Signin import Signin
from userManagement.AccountManagement import AccountManagement
from userManagement.ValidateRequest import ValidateRequest
from database.DB import DB
from threading import Thread
from DataManagement.Responder import Responder
from DataManagement.MessageItem import MessageItem
import os
from userManagement.FriendsManagement import FriendsManagement
from userManagement.Tokens import Tokens
from DataManagement.Leaderboard import Leaderboard
from Manifest import Manifest

class ProcessRequest:

    #PrecessReqeust is set up to be a seperate process in the OS and
    #will hold the shared request queue object. It will pull requests
    #from the queue as they are inserted from the listener
    def __init__(self, requestQueue):
        self.manifest = Manifest()
        reader = self.manifest.database_reader
        writer = self.manifest.database_writer
        username = self.manifest.database_username
        password = self.manifest.database_password
        userDatabase = self.manifest.user_database_name
        self.database = DB(username,password,reader,writer,userDatabase)
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
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)
            return

        parsedData = reqItem.parsedData

        if parsedData["requestType"] == "signin":
            token = self.signin.signin(parsedData, reqItem)
            print("Signin" + str(token))
            print("parsedData:",parsedData)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "createAccount":
            result = self.accountManager.createAccount(reqItem.parsedData)
            if result == True:
                reqItem.createAccountResponse('success')
            elif result == False:
                reqItem.createAccountResponse('fail')
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getUserStats":
            #call Account Management to get user stats
            self.accountManager.getUserStats(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "changePassword":
            #call Account Management to get user stats
            print("change password request called")
            self.accountManager.changePassword(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getFriendsList":
            #call FriendsManager to retrieve friends list
            self.friendsManager.getFriendsList(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "sendFriendRequest":
            #call FriendsManager to send friend request
            self.friendsManager.sendFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "validateFriendRequest":
            #call friends management to validate friend request
            self.friendsManager.validateFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getFriendRequests":
            #call friends management to validate friend request
            print("processing getFriendRequests")
            self.friendsManager.getFriendRequests(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "removeFriend":
            self.friendsManager.removeFriend(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "signout":
            self.signin.signout(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getMostChessGamesWon":
            self.leaderboard.getMostChessGamesWon(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getLongestWinStreak":
            self.leaderboard.getLongestWinStreak(reqItem, parsedData["numberOfGames"])
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "saveAccountInfoByKey":
            self.accountManager.saveAccountInfoByKey(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        # elif parsedData["requestType"] == "getAccountInfo":
        #    self.accountManager.getAccountInfo(parsedData)
        #    self.responder.sendResponse(reqItem)
        else:
            self.responder.sendBadRequest(reqItem.connectionSocket)


    #The process thread will block on requestQueue.get() until something
    #arrives.
    def processRequests(self):
        while True:
            requestItem = self.requestQueue.get()
            #Decrypt parsedData
            self.proccesRequestType(requestItem)
