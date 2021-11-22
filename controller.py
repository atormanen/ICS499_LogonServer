#!/usr/bin/env python3
import multiprocessing
from multiprocessing import Process
from threading import Thread
from global_logger import logged_method, logger
from listener import Listener
from manifest import Manifest
from process_request import ProcessRequest


# Controller will initialize all the objects and processes needed
# for the applications. It will spin up a few request request processors
# and then run the listener thread.
class Controller:

    # requestQueue is shared queue among all processes
    @logged_method
    def __init__(self):
        self.manifest = Manifest()
        self.request_queue = multiprocessing.Queue()
        self.listener = Listener(self.request_queue)

    @logged_method
    def create_request_processor(self):
        req = ProcessRequest(self.request_queue)
        req.process_requests()

    @logged_method
    def create_request_processors(self):
        processes = []
        for i in range(self.manifest.number_of_request_processors):
            logger.info(f"creating request processor {str(i)}")
            # print('Creating processes %d' % i)
            processes.append(Process(target=self.create_request_processor))
        for i in processes:
            i.start()

    @logged_method
    def create_listener(self):
        logger.info('creating request listener')
        self.listener.create_listener()
        thread = Thread(target=self.listener.listen)
        thread.start()
        thread.join()


if __name__ == '__main__':
    logger.info('')
    logger.info('starting logon server')
    logger.info('')
    c = Controller()
    c.create_request_processors()
    c.create_listener()
