from Listener import Listener
from database.MysqlDB import MysqlDB
from multiprocessing import Process
import multiprocessing
from threading import Thread
from ProcessRequest import ProcessRequest
import os
import queue

class Controller:
    #listener = ''

    def __init__(self):
        self.requestQueue = multiprocessing.Queue()
        self.listener = Listener(self.requestQueue)
        self.mysqlDB = MysqlDB('admin','ICS4992020','chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com','userdb')

    def createRequestProcessor(self):
        req = ProcessRequest(self.mysqlDB, self.requestQueue)
        req.processRequests()

    def createRequestProcessors(self):
        processes = []
        for i in range(os.cpu_count()):
            print('Createing processes %d' % i)
            processes.append(Process(target=self.createRequestProcessor))
        for i in processes:
            i.start()

    def createListener(self):
        self.listener.createListener()
        self.listener.listen()
        thread = Thread(target=listener.listen, args=(listener,))
        thread.start()
        thread.join()

def main():
    print('inside main')


if __name__ == '__main__':
    c = Controller()
    c.createRequestProcessors()
    c.createListener()
    main()
