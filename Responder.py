import socket
import sys
from RequestItem import RequestItem

#Responder will handle all the return messages for the servers
## TODO: clean this up... find a better way to implement responder
class Responder:

    def __init__(self):
        self.num = 0

    def sendBadRequest(self,connectionSocket):
        msg = "ERROR - BAD REQUEST"
        connectionSocket.send(msg.encode('utf-8'))
        #connectionSocket.close()

    def sendRequestedData(self,connectionSocket,reqestedData):
        connectionSocket.send(requestedData.encode())

    def sendAccountCreationStatus(self, connectionSocket,status):
        status = '' + status
        connectionSocket.send(status.encode())
