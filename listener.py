import json
import socket
from threading import Thread

from data.message_item import build_request
from global_logger import INFO, log
from manifest import Manifest
from process_request import *


# Class listener is used to listen on a servers ip address and port port_number
# 12345 for incoming requests.
class Listener:
    hostname = socket.gethostname()

    def __init__(self, request_queue):
        self.manifest = Manifest()
        self.request_queue = request_queue
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = self.manifest.listener_buffer_size
        self.port_number = self.manifest.port_number
        self.server_ip = ''
        self.req_count = 0

    def create_socket(self):

        log('creating server socket listener', level=INFO)
        try:
            self.server_socket.bind((self.server_ip, self.port_number))
            self.server_socket.listen(5)
        except OSError as error:
            log_error(error)
        log(f"server socket: {str(self.server_socket)}")

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
            log(f"server ip set to: {self.server_ip}", level=INFO)

    def send_bad_request(self, connection_socket):

        msg = "{'ERROR':'BAD REQUEST'}"
        connection_socket.send(msg.encode())

    def process_request(self, connection_socket):

        full_msg = ''
        received_msg = ''
        buffer_exceeded = False
        while True:
            if buffer_exceeded:
                try:
                    connection_socket.settimeout(3)
                    received_msg = connection_socket.recv(self.buffer_size).decode('utf-8', 'replace')
                except socket.timeout:
                    # Expecting a timeout
                    break
            else:
                try:

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
            log_error(error)
            return
        try:
            parsed_data = json.loads(full_msg)
        except (json.decoder.JSONDecodeError):
            log_error(f"unable to load message into json: {full_msg}")
            self.send_bad_request(connection_socket)
            return
        request = build_request(connection_socket, parsed_data)
        log(f"message item: {parsed_data}")
        self.request_queue.put(request)

    def listen(self):
        connection_socket = None
        while True:
            self.req_count += 1
            try:
                connection_socket, address = self.server_socket.accept()
                log(f"received message from {str(address)}")
                thread = Thread(target=self.process_request, args=(connection_socket,))
                thread.start()
            except IOError as error:
                log_error(error)
                if connection_socket:
                    connection_socket.close()

    def create_listener(self):

        self.set_ip()
        self.create_socket()
