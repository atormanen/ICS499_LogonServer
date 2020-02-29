from userManagement.Signin import Signin
from userManagement.AccountManagement import AccountManagement
from userManagement.ValidateRequest import ValidateRequest
from database.DB import DB
from threading import Thread
from DataManagement.Responder import Responder
import os
from userManagement.FriendsManagement import FriendsManagement

class ProcessRequest:

    #PrecessReqeust is set up to be a seperate process in the OS and
    #will hold the shared request queue object. It will pull requests
    #from the queue as they are inserted from the listener
    def __init__(self, requestQueue):
        #self.database = DB('admin','ICS4992020','chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com','userdb')
        self.database = DB('app','123','192.168.1.174','userdb')
        self.requestQueue = requestQueue
        self.signin = Signin(self.database)
        self.createAccount = AccountManagement(self.database)
        self.reqValidation = ValidateRequest()
        self.responder = Responder()

    ## TODO: find a better way to process these requests types.
    def proccesRequestType(self, reqItem):
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)

        parsedData = reqItem.parsedData

        if parsedData["requestType"] == "signin":
            self.signin.signin(parsedData)
            return False
        elif parsedData["requestType"] == "createAccount":
            result = self.createAccount.createAccount(reqItem.parsedData)
            if result == True:
                returnStatus = "AccountCreationSuccusful"
            elif result == False:
                returnStatus = "AccountCreationFailed"
            self.responder.sendAccountCreationStatus(reqItem.connectionSocket, returnStatus)
            return False
        elif parsedData["requestType"] == "getUserStats":
            return False
        elif parsedData["requestType"] == "getFriendsList":
            return False
        elif parsedData["requestType"] == "sendFriendRequest":
            return False
        elif parsedData["requestType"] == "validateFriendRequest":
            return False
        else:
            #self.requestQueue.put(RequestItem(connectionSocket,parsedData))
            return True

    #The process thread will block on requestQueue.get() until something
    #arrives.
    def processRequests(self):
        while True:
            requestItem = self.requestQueue.get()
            #Decrypt parsedData
            self.proccesRequestType(requestItem)
