from userManagement import *


class processRequest:
    signin = signin()
    createAccount = createAccount()
    requestType = ''
    parsedData = ''

    def proccesRequestType(self, parsedData):
        self.parsedData = parsedData
        if parsedData["requestType"] == "signin":
            signin.signin(parsedData)
        elif parsedData["requestType"] == "createAccount":
            createAccount.createAccount(parsedData)
        else:
            return True
