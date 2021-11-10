import json
import socket
from threading import Thread

from data.message_item import build_request
from global_logger import *
from manifest import Manifest


# Class listener is used to listen on a servers ip address and port port_number
# 12345 for incoming requests.
from util.threading import ThreadController


class Listener:
    hostname = socket.gethostname()

    def __init__(self, controller: ThreadController, request_queue, timeout_seconds: float):
        self.timeout_seconds = timeout_seconds
        self.request_queue = request_queue
        self.manifest = Manifest()
        self.controller = controller
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(timeout_seconds)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = self.manifest.listener_buffer_size
        self.port_number = self.manifest.port_number
        self.server_ip = ''
        self.req_count = 0


    @logged_method
    def create_socket(self):

        logger.info('creating server socket listener')
        try:
            self.server_socket.bind((self.server_ip, self.port_number))
            self.server_socket.listen(5)
        except OSError as error:
            logger.error(error)
        logger.debug(f"server socket: {str(self.server_socket)}")

    @logged_method
    def set_ip(self):
        ip = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except socket.error:
            ip = '127.0.0.1'
        finally:
            s.close()
            self.server_ip = ip
            # self.server_ip = '18.191.38.171'
            logger.info(f"server ip set to: {self.server_ip}")

    @logged_method
    def send_bad_request(self, connection_socket):

        msg = "{'ERROR':'BAD REQUEST'}"
        connection_socket.send(msg.encode())

    @logged_method
    def process_request(self, connection_socket):

        # we need to ensure that this will eventually recheck self.controller.should_stay_alive
        #   otherwise it could prevent the program from exiting properly. To do this we use a
        #   timeout value on any blocking calls that will wait.

        full_msg = ''
        received_msg = ''
        buffer_exceeded = False
        while self.controller.should_stay_alive:
            if buffer_exceeded:
                try:
                    connection_socket.settimeout(self.timeout_seconds)
                    received_msg = connection_socket.recv(self.buffer_size).decode('utf-8', 'replace')
                except TimeoutError:
                    # Expecting a timeout
                    break
            else:
                try:
                    connection_socket.settimeout(self.timeout_seconds)
                    received_msg = connection_socket.recv(self.buffer_size).decode('utf-8', 'replace')
                except UnicodeDecodeError:
                    self.send_bad_request(connection_socket)
            full_msg += received_msg
            if (len(received_msg) == 0):
                break
            elif len(received_msg) < self.buffer_size:
                break
            elif len(received_msg) == self.buffer_size:
                received_msg = ''
                buffer_exceeded = True
        try:
            if not (full_msg[0] == "{"):
                full_msg = full_msg[2::]
        except IndexError as error:
            logger.error(error)
            return
        try:
            parsed_data = json.loads(full_msg)
        except (json.decoder.JSONDecodeError):
            logger.error(f"unable to load message into json: {full_msg}")
            self.send_bad_request(connection_socket)
            return
        request = build_request(connection_socket, parsed_data)
        logger.debug(f"message item: {parsed_data}")
        self.request_queue.put(request, timeout=self.timeout_seconds)

    @logged_method
    def listen(self):

        # we need to ensure that this will eventually recheck self.controller.should_stay_alive
        #   otherwise it could prevent the program from exiting properly. To do this we use a
        #   timeout value on any blocking calls that will wait.

        connection_socket = None
        while self.controller.should_stay_alive:
            self.req_count += 1
            try:
                self.server_socket.settimeout(self.timeout_seconds)
                connection_socket, address = self.server_socket.accept()
                logger.debug(f"received message from {str(address)}")
                thread = Thread(target=self.process_request, args=(connection_socket,))
                thread.start()
            except IOError as error:
                logger.error(error)
                if connection_socket:
                    connection_socket.close()

    @logged_method
    def create_listener(self):

        self.set_ip()
        self.create_socket()
