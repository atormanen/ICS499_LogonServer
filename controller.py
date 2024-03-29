#!/usr/bin/env python3
import multiprocessing
import sys
from multiprocessing import Process
from threading import Thread

from database.db import DB
from database.mysql_db import MySQLDB
from global_logger import log, INFO
from listener import Listener
from manifest import Manifest
from process_request import RequestProcessor


# Controller will initialize all the objects and processes needed
# for the applications. It will spin up a few request request processors
# and then run the listener thread.
class Controller:

    # requestQueue is shared queue among all processes
    def __init__(self, database: DB):
        if not isinstance(database, DB):
            raise TypeError('Controller was not supplied a DB object')
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
            log(f"creating request processor {str(i)}", level=INFO)
            # print('Creating processes %d' % i)
            processes.append(Process(target=self._create_request_processor))
        for i in processes:
            i.start()

    def create_listener(self):
        log('creating request listener', level=INFO)
        self.listener.create_listener()
        thread = Thread(target=self.listener.listen)
        thread.start()
        thread.join()


if __name__ == '__main__':
    args = sys.argv[1:]
    log(level=INFO)
    log('starting logon server', level=INFO)
    log(level=INFO)
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
    c = Controller(db)

    # Start the threads and/or processes
    c.create_request_processors()
    c.create_listener()
