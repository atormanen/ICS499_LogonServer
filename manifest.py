import os


class Manifest:

    def __init__(self):
        # Port number that the server will serve requests from
        self.port_number = 12345

        # Buffer size for the socket listening on port number above
        self.listener_buffer_size = 10240

        # Username to connect to the database
        self.database_username = 'admin'

        # Password used to connect to the database
        self.database_password = 'ICS4992020'

        # Name of the user database to connect too
        # noinspection SpellCheckingInspection
        self.user_database_name = 'userdb'

        # Name of the reader endpoint
        # noinspection SpellCheckingInspection
        self.database_reader = 'chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com'

        # name of the writer endpoint
        # noinspection SpellCheckingInspection
        self.database_writer = 'chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com'

        # Set the number of request processor processes that will be available
        # to work requests as they come in.
        self.number_of_request_processors = os.cpu_count()
