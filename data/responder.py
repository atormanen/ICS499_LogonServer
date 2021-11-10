from data.message_item import BaseRequest
from global_logger import logger, logged_method


# from MessageItem import MessageItem

# Responder will handle all the return messages for the servers
# TODO: clean this up... find a better way to implement responder
class Responder:

    def __init__(self):
        self.num = 0

    @logged_method
    def send_bad_request(self, connection_socket):

        logger.verbose(f"bad request")
        msg = "ERROR - BAD REQUEST"
        connection_socket.send(msg.encode('utf-8'))
        connection_socket.close()

    @logged_method
    def send_requested_data(self, connection_socket, requested_data):

        logger.error('sendRequestedData is deprecated... do not use!')
        connection_socket.send(requested_data.encode())

    @logged_method
    def send_account_creation_status(self, connection_socket, status):

        logger.error('sendAccountCreationStatus is deprecated... do not use!')
        status = '' + status
        connection_socket.send(status.encode())

    @logged_method
    def send_response(self, msg_item: BaseRequest, timeout_seconds: float):

        logger.debug(msg_item.response)
        try:
            msg_item.socket.settimeout(timeout_seconds)
            msg_item.socket.send(msg_item.response.encode())
        except ConnectionResetError as e:
            logger.error(e)
