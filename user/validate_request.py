from data.message_item import RequestType

# Validate request will check the initial variable to see what kind of request
# type it is.
# TODO: Check the entire json object for appropriate fields and not just the req type
from global_logger import logged_method


class RequestValidator:

    def __init__(self):
        self.num = 0

    @logged_method
    def is_bad_request(self, parsed_data):

        # If any check returns True, the request is considered bad
        requirement_check_list = [
            # valid request type
            lambda: parsed_data['request_type'] not in RequestType.get_items()
        ]
        for requirement_check in requirement_check_list:
            if requirement_check():
                return True
        return False
