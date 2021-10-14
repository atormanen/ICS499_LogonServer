from data.message_item import RequestType
from global_logger import logger, VERBOSE
import inspect


#Validate request will check the initial variable to see what kind of request
#type it is.
## TODO: Check the entire json object for apropriate fields and not just the req type
class RequestValidator:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self):
        self.num = 0

    def is_bad_request(self, parsed_data):
        self.log_function_name()

        # If any check returns True, the request is considered bad
        requirement_check_list = [
            # valid request type
            lambda: parsed_data['request_type'] not in RequestType.get_items()
        ]
        for requirement_check in requirement_check_list:
            if requirement_check():
                return True
        return False
