import socket
import sys
from database.mysqlDB import mysqlDB
from _thread import *
import threading
import json
from processRequest import *

db = mysqlDB('ICS499','CarmenDiane2019!','127.0.0.1','WeatherDataTest')
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
serverIp = '18.220.27.139'
#serverIp = '192.168.1.174'
portNumber = 12345
bufferSize = 1024
processReq = processRequest()

serverSocket.bind((serverIp,portNumber))
serverSocket.listen(5)
print("Server Initialized on ", serverIp, ":", portNumber)

def sendBadRequest(connectionSocket):
    #print("Error-bad request")
    msg = "ERROR - BAD REQUEST"
    connectionSocket.send(msg.encode())

def processRequest(connectionSocket):
    full_msg = ''
    rcvd_msg = ''
    bufferExceeded = False
    while True:
        if bufferExceeded:
            try:
                connectionSocket.settimeout(3)
                rcvd_msg = connectionSocket.recv(bufferSize).decode()
            except socket.timeout as err:
                #Expecting a timeout
                break
        else:
            rcvd_msg = connectionSocket.recv(bufferSize).decode()
        full_msg += rcvd_msg
        if(len(rcvd_msg) == 0):
            break
        elif len(rcvd_msg) < bufferSize:
            break
        elif len(rcvd_msg) == bufferSize:
            rcvd_msg = ''
            bufferExceeded = True
    #print(full_msg)
    try:
        parsedData = json.loads(full_msg)
    except (json.decoder.JSONDecodeError):
        sendBadRequest(connectionSocket)
        return
    #returns true if bad request
    if(processReq.proccesRequestType(parsedData)):
        sendBadRequest(connectionSocket)

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        counter = 0
        start_new_thread(processRequest, (connectionSocket,))
        #db.mysqlDump(full_msg)
    except IOError:
        print("IOError")
        connectionSocket.close()
