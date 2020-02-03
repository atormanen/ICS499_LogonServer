from userManagement.Signin import Signin
from userManagement.CreateAccount import CreateAccount
from database.MysqlDB import MysqlDB
from threading import Thread

class ProcessRequest:
    requestType = ''
    parsedData = ''

    def __init__(self, database, requestQueue):
        self.requestQueue = requestQueue
        self.database = database
        self.signin = Signin(self.database)
        self.createAccount = CreateAccount(self.database)

    def proccesRequestType(self, parsedData):
        self.parsedData = parsedData
        if parsedData["requestType"] == "signin":
            self.signin.signin(parsedData)
        elif parsedData["requestType"] == "createAccount":
            self.createAccount.createAccount(parsedData)
        else:
            return True
    def processRequests(self):
        requestItem = self.requestQueue.get()
        thread = Thread(target=self.proccesRequestType, args=(requestedItem.parsedData,))
        thread.start()
