from global_logger import logger, VERBOSE
import socket
import sys
#from _thread import *
from threading import Thread
import json
from ProcessRequest import *
from multiprocessing import Process
from DataManagement.MessageItem import MessageItem
from Manifest import Manifest
import inspect

#Class listener is used to listen on a servers ip address and port portNumber
#12345 for incoming requests.
class Listener:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")
    hostname = socket.gethostname()

    def __init__(self, requestQueue):
        self.manifest = Manifest()
        self.requestQueue = requestQueue
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bufferSize = self.manifest.listener_buffer_size
        self.portNumber = self.manifest.port_number
        self.serverIp = ''
        self.reqCount = 0

    def createSocket(self):
        self.log_function_name()
        logger.info('creating server socker listener')
        self.serverSocket.bind((self.serverIp,self.portNumber))
        self.serverSocket.listen(5)
        logger.debug(f"server socket: {str(self.serverSocket)}")

    def set_ip(self):
        self.log_function_name()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
            self.serverIp = IP
            logger.info(f"server ip set to: {self.serverIp}")


    def sendBadRequest(self,connectionSocket):
        self.log_function_name()
        msg = "{'ERROR':'BAD REQUEST'}"
        connectionSocket.send(msg.encode())

    def processRequest(self,connectionSocket):
        self.log_function_name()
        full_msg = ''
        rcvd_msg = ''
        bufferExceeded = False
        while True:
            if bufferExceeded:
                try:
                    connectionSocket.settimeout(3)
                    rcvd_msg = connectionSocket.recv(self.bufferSize).decode('utf-8','replace')
                except socket.timeout as err:
                    #Expecting a timeout
                    break
            else:
                try:

                    rcvd_msg = connectionSocket.recv(self.bufferSize).decode('utf-8','replace')
                except UnicodeDecodeError:
                    self.sendBadRequest(connectionSocket)
            full_msg += rcvd_msg
            if(len(rcvd_msg) == 0):
                break
            elif len(rcvd_msg) < self.bufferSize:
                break
            elif len(rcvd_msg) == self.bufferSize:
                rcvd_msg = ''
                bufferExceeded = True
        try:
            if not (full_msg[0] == "{"):
                full_msg = full_msg[2::]
        except IndexError as error:
            logger.error(error)
            return

        try:
            parsedData = json.loads(full_msg)
        except (json.decoder.JSONDecodeError):
            logger.error(f"unable to load message into json: {parsedData}")
            self.sendBadRequest(connectionSocket)
            return
        msgItem = MessageItem(connectionSocket,parsedData)
        logger.debug(f"message item: {msgItem}")
        self.requestQueue.put(msgItem)


    def listen(self):
        self.log_function_name()
        while True:
            self.reqCount = self.reqCount + 1
            try:
                connectionSocket, addr = self.serverSocket.accept()
                logger.debug(f"received message from {str(addr)}")
                thread = Thread(target=self.processRequest,args=(connectionSocket,))
                thread.start()
            except IOError as error:
                logger.error(error)
                connectionSocket.close()

    def createListener(self):
        self.log_function_name()
        self.set_ip()
        self.createSocket()
