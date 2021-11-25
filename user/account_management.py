# Is this class necessary? Should it be combined with signin?
import time
from global_logger import logged_method
from data.message_item import GetUserStatsRequest, ChangePasswordRequest, SaveAccountInfoByKeyRequest, \
    CreateAccountRequest


class AccountManagement:

    username = ''
    password = ''

    def __init__(self, mysql_d_b):
        self.db = mysql_d_b

    def validate_username(self, username):
        if (self.db.user_exists(username)):
            return True
        return False

    def is_password_valid(self, password):
        upper_ctr, lower_ctr, number_ctr, special_ctr = 0, 0, 0, 0

        for i in range(len(password)):
            if 'A' <= password[i] <= 'Z':
                upper_ctr += 1
            elif 'a' <= password[i] <= 'z':
                lower_ctr += 1
            elif '0' <= password[i] <= '9':
                number_ctr += 1
            else:
                special_ctr += 1
        number_of_good_char = upper_ctr + number_ctr + special_ctr

        if (number_of_good_char >= 3):
            return True
        else:
            return False

    def create_account(self, req_item: CreateAccountRequest):
        parsed_data = req_item.parsed_data
        # check if username exists
        result = self.db.username_is_available(parsed_data["username"])

        # call mysql_d_b to create CreateAccount
        if not result:
            self.db.create_user(parsed_data)
            req_item.set_response()
        else:
            req_item.set_response(failure_reason='username already exists')

    def get_user_stats(self, req_item: GetUserStatsRequest):
        stats = self.db.get_user_stats(req_item.username)
        req_item.set_response(stats=stats[0])

    def validate_password(self, username, password):
        if (self.db.user_exists(username)):
            db_password = self.db.get_password_for(username)
            db_password = db_password[0][0]
            # compare password to given get_password
            if (password == db_password):
                return True
        return False

    def token_up_to_date(self, username):
        token_expiration = self.db.get_token_creation_time(username)
        # if(token_expiration):
        #    return False
        current_time = time.time()
        time_difference = current_time - token_expiration[0][0]
        if (time_difference > 86400):
            return False
        return True

    def change_password(self, req_item: ChangePasswordRequest):
        username = req_item.username
        # signon_token = parsed_data["signon_token"]
        old_password = req_item.old_password
        new_password = req_item.new_password
        if self.validate_password(username, old_password):
            # TODO remove commented out code if it is not needed
            # if(True):
            saved_password = self.db.get_password_for(username)
            saved_password = saved_password[0][0]

            if (saved_password == old_password):
                self.db.change_password(username, new_password)
                req_item.set_response()
            else:
                req_item.set_response(failure_reason='Provided previous password was not a match')
        else:
            req_item.set_response(failure_reason='Unable to validate password.')

    def save_account_info_by_key(self, req_item: SaveAccountInfoByKeyRequest):
        username = req_item.username
        hash_val = req_item.hash_val
        key = req_item.key
        value = req_item.value

        # # FIXME remove if not needed
        # signon_token = req_item.signon_token
        # type_val = req_item.type_val

        if (self.validate_password(username, hash_val)):
            self.db.SaveAccountInfoByKey(username, key, value)
            req_item.set_response()
        else:
            req_item.set_response(failure_reason="Unable to validate password")
