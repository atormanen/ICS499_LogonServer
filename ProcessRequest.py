from userManagement.Signin import Signin
from userManagement.CreateAccount import CreateAccount
from userManagement.Validation import Validation
from database.MysqlDB import MysqlDB
from threading import Thread
from Responder import Responder
import os
from userManagement.FriendsManagement import *

class ProcessRequest:
    requestType = ''
    parsedData = ''

    def __init__(self, requestQueue):
        self.requestQueue = requestQueue
        self.signin = Signin(self.database)
        self.createAccount = CreateAccount(self.database)
        self.reqValidation = Validation()
        self.responder = Responder()
        self.mysqlDB = MysqlDB('admin','ICS4992020','chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com','userdb')

    def proccesRequestType(self, reqItem):
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)
        if parsedData["requestType"] == "signin":
            #self.sendBadRequest(connectionSocket)
            return False
        elif parsedData["requestType"] == "createAccount":
            self.createAccount.createAccount(reqItem.parsedData)
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

    def processRequests(self):
        while True:
            #print("waiting on req queue - PID: ", os.getpid())
            requestItem = self.requestQueue.get()

            #Decrypt parsedData

            self.proccesRequestType(requestItem)
