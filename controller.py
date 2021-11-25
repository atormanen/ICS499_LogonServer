#!/usr/bin/env python3
import multiprocessing
import sys
from multiprocessing import Process
from threading import Thread
from typing import Optional

from database.db import DB
from database.mysql_db import MySQLDB
from global_logger import logger, log_error
from listener import Listener
from manifest import Manifest
from process_request import RequestProcessor


# Controller will initialize all the objects and processes needed
# for the applications. It will spin up a few request request processors
# and then run the listener thread.
class Controller:

    # requestQueue is shared queue among all processes
    def __init__(self, database: Optional[DB] = None):
        self.manifest = Manifest()
        self.request_queue = multiprocessing.Queue()
        self.listener = Listener(self.request_queue)
        self.database = database

    def _create_request_processor(self):
        req = RequestProcessor(self.request_queue, self.database)
        req.process_requests()


    def create_request_processors(self):
        processes = []
        for i in range(self.manifest.number_of_request_processors):
            logger.info(f"creating request processor {str(i)}")
            # print('Creating processes %d' % i)
            processes.append(Process(target=self._create_request_processor))
        for i in processes:
            i.start()

    def create_listener(self):
        logger.info('creating request listener')
        self.listener.create_listener()
        thread = Thread(target=self.listener.listen)
        thread.start()
        thread.join()


if __name__ == '__main__':
    try:
        raise TypeError('test')
    except BaseException as e:
        log_error(e)
    args = sys.argv[1:]
    logger.info('')
    logger.info('starting logon server')
    logger.info('')
    if args:
        # get database configuration info from arguments and password from input.
        from getpass import getpass
        db_implementation, host, username, db_name, *_ = args
        password = getpass(prompt='Enter database password: ')
    else:
        # load database configuration from params.json file.
        import json
        with open('./params.json', 'r') as f:
            data = json.loads(f.read())
        db_implementation = 'mysql'
        host = data['db_host']
        username = data['db_username']
        password = data['db_password']
        db_name = data['db_name']

    # Set up the database object based on database implementation selected
    db = {'mysql': MySQLDB(username, password, host, host, db_name)}[db_implementation]

    # Setup the controller.
    c = Controller()

    # Start the
    c.create_request_processors()
    c.create_listener()

