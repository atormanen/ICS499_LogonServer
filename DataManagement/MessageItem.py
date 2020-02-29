import json
#Request item is a wrapper class to hold the data of each reqeust.
#It holds the json object that was sent to the server as well as
#the socket

class MessageItem:
    def __init__(self,connectionSocket, parsedData):
        self.connectionSocket = connectionSocket
        self.parsedData = parsedData
