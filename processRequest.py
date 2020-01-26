from userManagement.Signin import Signin
from userManagement.CreateAccount import CreateAccount
from database.MysqlDB import MysqlDB


class processRequest:
    mysqlDB = ''
    signin = ''
    createAccount = ''
    requestType = ''
    parsedData = ''

    def __init__(self):
        self.mysqlDB = MysqlDB('admin','ICS4992020','chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com','userdb')
        self.signin = Signin(self.mysqlDB)
        self.createAccount = CreateAccount(self.mysqlDB)

    def proccesRequestType(self, parsedData):
        self.parsedData = parsedData
        if parsedData["requestType"] == "signin":
            self.signin.signin(parsedData)
        elif parsedData["requestType"] == "createAccount":
            self.createAccount.createAccount(parsedData)
        else:
            return True
