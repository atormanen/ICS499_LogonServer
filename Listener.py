import socket
import sys
#from _thread import *
from threading import Thread
import json
from ProcessRequest import *
from multiprocessing import Process
from RequestItem import RequestItem

#Class listener is used to listen on a servers ip address and port portNumber
#12345 for incoming requests.
class Listener:
    hostname = socket.gethostname()

    def __init__(self, requestQueue):
        self.requestQueue = requestQueue
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bufferSize = 1024
        self.portNumber = 12345
        self.serverIp = ''
        self.reqCount = 0

    def createSocket(self):
        self.serverSocket.bind((self.serverIp,self.portNumber))
        self.serverSocket.listen(5)
        #print("Server Initialized on ", self.serverIp, ":", self.portNumber)

    def set_ip(self):
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


    def sendBadRequest(self,connectionSocket):
        #print("Error-bad request")
        msg = "ERROR - BAD REQUEST"
        connectionSocket.send(msg.encode())

    def processRequest(self,connectionSocket):
        full_msg = ''
        rcvd_msg = ''
        bufferExceeded = False
        while True:
            if bufferExceeded:
                try:
                    connectionSocket.settimeout(3)
                    rcvd_msg = connectionSocket.recv(self.bufferSize).decode()
                except socket.timeout as err:
                    #Expecting a timeout
                    break
            else:
                rcvd_msg = connectionSocket.recv(self.bufferSize).decode()
            full_msg += rcvd_msg
            if(len(rcvd_msg) == 0):
                break
            elif len(rcvd_msg) < self.bufferSize:
                break
            elif len(rcvd_msg) == self.bufferSize:
                rcvd_msg = ''
                bufferExceeded = True
        print("TEST",full_msg)
        try:
            parsedData = json.loads(full_msg)
        except (json.decoder.JSONDecodeError):
            self.sendBadRequest(connectionSocket)
            #print("Badd req from listener")
            return
        reqItem = RequestItem(connectionSocket,parsedData)
        self.requestQueue.put(reqItem)


    def listen(self):
        while True:
            #print(counter)
            selr.reqCount = reqCount + 1
            try:
                connectionSocket, addr = self.serverSocket.accept()
                thread = Thread(target=self.processRequest,args=(connectionSocket,))
                thread.start()
                #is thread.join nececary?
                thread.join()
            except IOError:
                #print('IOError')
                connectionSocket.close()

    def createListener(self):
        self.set_ip()
        self.createSocket()
