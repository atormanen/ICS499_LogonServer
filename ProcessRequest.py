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

class ProcessRequest:

    #PrecessReqeust is set up to be a seperate process in the OS and
    #will hold the shared request queue object. It will pull requests
    #from the queue as they are inserted from the listener
    def __init__(self, requestQueue):
        #self.database = DB('admin','ICS4992020','chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com','userdb')
        self.database = DB('app','123','192.168.1.174','userdb')
        self.requestQueue = requestQueue
        self.signin = Signin(self.database)
        self.accountManagement = AccountManagement(self.database)
        self.friendsManagement = FriendsManagement(self.database)
        self.reqValidation = ValidateRequest()
        self.responder = Responder()

    ## TODO: find a better way to process these requests types.
    def proccesRequestType(self, reqItem):
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)

        parsedData = reqItem.parsedData

        if parsedData["requestType"] == "signin":
            token = self.signin.signin(parsedData)
            reqItem.signinResponse(token)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "createAccount":
            result = self.accountManagement.createAccount(reqItem.parsedData)
            if result == True:
                reqItem.createAccountResponse('succus')
            elif result == False:
                reqItem.createAccountResponse('fail')
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getUserStats":
            #call Account Management to get user stats
            self.accountManagement.getUserStats(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "getFriendsList":
            #call FriendsManagement to retrieve friends list
            self.friendsManagement.getFriendsList(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "sendFriendRequest":
            #call FriendsManagement to send friend request
            self.friendsManagement.sendFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        elif parsedData["requestType"] == "validateFriendRequest":
            #call friends management to validate friend request
            self.friendsManagement.validateFriendRequest(parsedData, reqItem)
            self.responder.sendResponse(reqItem)
        else:
            self.responder.sendBadRequest(reqItem.connectionSocket)


    #The process thread will block on requestQueue.get() until something
    #arrives.
    def processRequests(self):
        while True:
            requestItem = self.requestQueue.get()
            #Decrypt parsedData
            self.proccesRequestType(requestItem)
