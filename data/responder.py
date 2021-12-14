from socket import socket

from data.message_item import BaseRequest
from global_logger import log, VERBOSE, deprecated, log_error


# from MessageItem import MessageItem

# Responder will handle all the return messages for the servers
# TODO: clean this up... find a better way to implement responder
class Responder:

    def __init__(self, timeout_seconds: float):
        self.num = 0
        self.timeout_seconds = timeout_seconds

    def send_bad_request(self, connection_socket: socket):
        connection_socket.settimeout(self.timeout_seconds)
        log(f"bad request", level=VERBOSE)
        msg = "ERROR - BAD REQUEST"
        connection_socket.send(msg.encode('utf-8'))
        connection_socket.close()

    @deprecated
    def send_requested_data(self, connection_socket: socket, requested_data):
        warn('This is deprecated.', DeprecationWarning)
        connection_socket.settimeout(self.timeout_seconds)
        connection_socket.send(requested_data.encode())

    @deprecated
    def send_account_creation_status(self, connection_socket: socket, status):
        warn('This is deprecated.', DeprecationWarning)
        connection_socket.settimeout(self.timeout_seconds)
        status = '' + status
        connection_socket.send(status.encode())

    def send_response(self, msg_item: BaseRequest, timeout_seconds: float):
        log(f'response: {msg_item.response}')
        try:
            msg_item.socket.settimeout(timeout_seconds)
            msg_item.socket.send(msg_item.response.encode())
        except ConnectionResetError as e:
            log_error(e, 'connection reset')
