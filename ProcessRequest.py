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

    def __init__(self, database, requestQueue):
        self.requestQueue = requestQueue
        self.database = database
        self.signin = Signin(self.database)
        self.createAccount = CreateAccount(self.database)
        self.reqValidation = Validation()
        self.responder = Responder()

    def proccesRequestType(self, reqItem):
        if self.reqValidation.isBadRequest(reqItem.parsedData):
            self.responder.sendBadRequest(reqItem.connectionSocket)

    def processRequests(self):
        while True:
            print("waiting on req queue - PID: ", os.getpid())
            requestItem = self.requestQueue.get()

            #Decrypt parsedData

            self.proccesRequestType(requestItem)
