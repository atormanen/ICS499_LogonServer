#!/usr/bin/env python3
import queue
from threading import Thread, RLock, Condition
from typing import List

from global_logger import *
from listener import Listener
from manifest import Manifest
from process_request import RequestProcessor

# Controller will initialize all the objects and processes needed
# for the applications. It will spin up a few request request processors
# and then run the listener thread.

LISTENER_TIMEOUT_SECONDS = 3.0
REQUEST_PROCESSOR_TIMEOUT_SECONDS = 3.0


class Controller:

    # requestQueue is shared queue among all processes
    @logged_method
    def __init__(self):
        try:
            self._error = None
            self._should_stay_alive = True
            self.lock = RLock()
            self.condition = Condition(self.lock)
            self.manifest = Manifest()
            self.request_queue = queue.Queue()
            self.listener = Listener(self, self.request_queue, LISTENER_TIMEOUT_SECONDS)
            self.processor_threads: List[Thread] = []
            self.create_request_processors()
            self.listener_thread = self.create_listener()

            self._wait_until_no_longer_should_stay_alive()
        finally:
            self.should_stay_alive = False  # ensures that all threads will eventually stop
            if self.error:
                e_msg = f'Shutting down with error {self.error!r}'
                log_error(self.error, e_msg)
            logger.info('')
            logger.info(f'stopping logon server (pid={os.getpid()})')
            logger.info('')

            for i in range(len(self.processor_threads)):
                logger.debug(f'trying to join processor thread {i + 1} of {len(self.processor_threads)}...')
                self.processor_threads[i].join()
                logger.debug(f'finished to join processor thread {i + 1} of {len(self.processor_threads)}')

            logger.debug('trying to join Listener thread ...')
            self.listener_thread.join()
            logger.debug('finished to join Listener thread ...')

    @property
    def error(self) -> BaseException:
        with self.condition:
            return self._error

    @error.setter
    def error(self, value):
        with self.condition:
            self._error = value
            self.condition.notify_all()

    @property
    def should_stay_alive(self):
        with self.condition:
            return self._should_stay_alive

    @should_stay_alive.setter
    def should_stay_alive(self, value):
        with self.condition:
            self._should_stay_alive = value
            self.condition.notify_all()

    def _wait_until_no_longer_should_stay_alive(self):
        with self.condition:
            while self._should_stay_alive:
                self.condition.wait()

    @logged_method
    def create_request_processor(self):
        allowed_retries = 5
        retries = 0
        try:
            req = RequestProcessor(self, self.request_queue, REQUEST_PROCESSOR_TIMEOUT_SECONDS)
            req.process_requests()
        except RuntimeError as e:
            if retries < allowed_retries:
                retries += 1
            else:
                self.error = e
                self.should_stay_alive = False
        except BaseException as e:
            if retries < allowed_retries:
                retries += 1
            else:
                self.error = e
                self.should_stay_alive = False


    @logged_method
    def create_request_processors(self):
        for i in range(self.manifest.number_of_request_processors):
            logger.info(f"creating request processor {str(i)}")
            # print('Creating processes %d' % i)
            self.processor_threads.append(
                Thread(target=self.create_request_processor, name=f'req_processor_thread_{i}'))
        for i in self.processor_threads:
            i.start()

    @logged_method
    def create_listener(self):
        logger.info('creating request listener')
        self.listener.create_listener()
        thread = Thread(target=self.listener.listen, name='listener_thread')
        thread.start()
        return thread
        # thread.join()


if __name__ == '__main__':
    logger.info('')
    logger.info('starting logon server')
    logger.info('')
    c = Controller()
