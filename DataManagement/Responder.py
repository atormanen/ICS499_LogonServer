import socket
import sys
from global_logger import logger, VERBOSE
import inspect
#from MessageItem import MessageItem

#Responder will handle all the return messages for the servers
## TODO: clean this up... find a better way to implement responder
class Responder:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self):
        self.num = 0

    def sendBadRequest(self,connectionSocket):
        self.log_function_name()
        logger.verbose(f"bad request")
        msg = "ERROR - BAD REQUEST"
        connectionSocket.send(msg.encode('utf-8'))
        connectionSocket.close()


    def sendRequestedData(self,connectionSocket,reqestedData):
        self.log_function_name()
        logger.error('sendRequestedData is deprecated... do not use!')
        connectionSocket.send(requestedData.encode())


    def sendAccountCreationStatus(self, connectionSocket,status):
        self.log_function_name()
        logger.error('sendAccountCreationStatus is deprecated... do not use!')
        status = '' + status
        connectionSocket.send(status.encode())


    def sendResponse(self, msgItem):
        self.log_function_name()
        logger.debug(msgItem.responseObj)
        try:
            msgItem.connectionSocket.send(msgItem.responseObj.encode())
        except ConnectionResetError as e:
            logger.error(e)
