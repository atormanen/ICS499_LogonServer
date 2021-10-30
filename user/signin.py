import time

from global_logger import logger, logged_method
from user.tokens import Tokens


# Signin will handle the mechanics of signing a user in
class Signin:

    def __init__(self, db):
        self.db = db
        self.token = Tokens()

    @logged_method
    def validate_password(self, username, password):

        if (self.db.validate_user_exists(username)):
            db_password = self.db.get_password_for(username)
            db_password = db_password[0][0]
            # compare password to given get_password
            if (password == db_password):
                return True
        return False

    @logged_method
    def token_up_to_date(self, username):

        token_expiration = self.db.get_token_creation_time(username)
        # if(token_expiration):
        #    return False
        current_time = time.time()
        time_difference = current_time - token_expiration[0][0]
        if (time_difference > 86400):
            logger.debug(f"token expired for user {username}")
            return False
        logger.debug(f"token is valid for user {username}")
        return True

    @logged_method
    def signin(self, parsed_data, req_item):

        username = parsed_data["username"]
        password = parsed_data["password"]
        data = self.get_account_info(parsed_data)

        if (self.validate_password(username, password)):
            if (self.token_up_to_date(username)):
                # Bundle the token into the response package
                signon_token = self.db.get_token(username)
                signon_token = signon_token[0][0]
                logger.debug(type(signon_token))
                if (signon_token is None):
                    signon_token = self.token.get_token()
                    self.db.signin(username, signon_token, self.token.get_token_creation_time())
                req_item.set_signin_response(signon_token, data)
            else:
                signon_token = self.token.get_token()
                self.db.signin(username, signon_token, self.token.get_token_creation_time())
                req_item.set_signin_response(signon_token, data)
        else:
            logger.debug(f"signin failed for user {username}")
            req_item.set_signin_response_failed('invalid password')

    @logged_method
    def signout(self, parsed_data, req_item):

        username = parsed_data["username"]
        signon_token = parsed_data["signon_token"]
        saved_token = self.db.get_token(username)
        saved_token = saved_token[0][0]
        if saved_token is None:
            req_item.set_signout_response(was_successful=False,
                                          failure_reason='currently not logged in')
            return

        self.db.logout(username)
        self.db.save_account_info(username, parsed_data)
        req_item.set_signout_response(was_successful=True)

    @logged_method
    def get_account_info(self, parsed_data):

        username = parsed_data["username"]
        # signon_token = parsed_data["signonToken"]
        data = self.db.get_account_info(username)
        return data
