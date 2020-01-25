from userManagement import signin


class processRequest:
    requestType = ''
    parsedData = ''
    signin = signin()
    lobby = lobby()
    gameMangement = move()

    def proccesRequestType(self, parsedData):
        if parsedData["requestType"] == "signin":
            signin.signin()
        elif parsedData["requestType"] == "lobby":
            lobby.lobby()
        elif parsedData["requestType"] == "move":
            print(parsedData["requestType"])
        elif parsedData["requestType"] == "leaderboards":
            print(parsedData["requestType"])
        elif parsedData["requestType"] == "createAccount":
            print(parsedData["requestType"])
        else:
            return True
