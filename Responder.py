import socket
import sys
from RequestItem import RequestItem

class Responder:

    def __init__(self):
        self.num = 0

    def sendBadRequest(self,connectionSocket):
        msg = "ERROR - BAD REQUEST"
        connectionSocket.send(msg.encode())
        #connectionSocket.close()

    def sendRequestedData(self,connectionSocket,reqestedData):
        connectionSocket.send(requestedData.encode())

    def sendAccountCreationStatus(self, connectionSocket,status):
        status = '' + status
        connectionSocket.send(status.encode())
