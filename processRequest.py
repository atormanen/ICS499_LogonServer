from userManagement.signin import signin
from userManagement.createAccount import createAccount


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
