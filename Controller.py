from global_logger import logger, VERBOSE
from Listener import Listener
from database.DB import DB
from multiprocessing import Process
import multiprocessing
from threading import Thread
from ProcessRequest import ProcessRequest
import os
import queue
import inspect

#Controller will initilaize all the objects and processes needed
#for the applications. It will sping up a few request request processors
#and then run the listener thread.
class Controller:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    # requestQueue is shared queue among all processes
    def __init__(self):
        self.requestQueue = multiprocessing.Queue()
        self.listener = Listener(self.requestQueue)
        self.number_of_request_processors = os.cpu_count()


    def createRequestProcessor(self):
        self.log_function_name()
        req = ProcessRequest(self.requestQueue)
        req.processRequests()


    def createRequestProcessors(self):
        self.log_function_name()
        processes = []
        for i in range(self.number_of_request_processors):
            logger.info(f"creating request processor {str(i)}")
            #print('Createing processes %d' % i)
            processes.append(Process(target=self.createRequestProcessor))
        for i in processes:
            i.start()


    def createListener(self):
        self.log_function_name()
        logger.info('creating request listener')
        self.listener.createListener()
        thread = Thread(target=self.listener.listen)
        thread.start()
        thread.join()


if __name__ == '__main__':
    logger.info('')
    logger.info('starting logon server')
    logger.info('')
    c = Controller()
    c.createRequestProcessors()
    c.createListener()
