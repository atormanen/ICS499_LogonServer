# Is this class necessary? Should it be combined with signin?
import time
from global_logger import logged_method


class AccountManagement:

    username = ''
    password = ''

    def __init__(self, mysql_d_b):
        self.db = mysql_d_b

    @logged_method
    def validate_username(self, username):
        if (self.db.user_exists(username)):
            return True
        return False

    @logged_method
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

    @logged_method
    def create_account(self, req_item):
        parsed_data = req_item.parsed_data
        # check if username exists
        result = self.db.username_is_available(parsed_data["username"])

        # call mysql_d_b to create CreateAccount
        if not result:
            self.db.create_user(parsed_data)
            req_item.set_create_account_response(True)
        else:
            req_item.set_create_account_response(False, 'username already exists')

    @logged_method
    def get_user_stats(self, parsed_data, req_item):
        stats = self.db.get_user_stats(parsed_data["username"])
        req_item.set_get_user_stats_response(stats[0])

    @logged_method
    def validate_password(self, username, password):
        if (self.db.user_exists(username)):
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
            return False
        return True

    @logged_method
    def change_password(self, parsed_data, req_item):
        username = parsed_data["username"]
        # signon_token = parsed_data["signon_token"]
        old_password = parsed_data["old_password"]
        new_password = parsed_data["new_password"]
        if self.validate_password(username, old_password):
            # TODO remove commented out code if it is not needed
            # if(True):
            saved_password = self.db.get_password_for(username)
            saved_password = saved_password[0][0]

            if (saved_password == old_password):
                self.db.change_password(username, new_password)
                req_item.set_change_password_response(was_successful=True)
            else:
                req_item.set_change_password_response(was_successful=False,
                                                      failure_reason='Provided previous password was not a match')
        # else:
        #     print("token is not up to date")
        #     req_item.set_change_password_response("fail")
        else:
            req_item.set_change_password_response(was_successful=False,
                                                  failure_reason='Unable to validate password.')

    @logged_method
    def save_account_info_by_key(self, parsed_data, req_item):
        username = parsed_data["username"]
        signon_token = parsed_data["signon_token"]
        hash_val = parsed_data["hash"]
        key = parsed_data["key"]
        value = parsed_data["value"]
        type_val = parsed_data["type"]
        if (self.validate_password(username, hash_val)):
            self.db.save_account_info_by_key(username, key, value)
            req_item.set_save_account_info_by_key_response(was_successful=True)
        else:
            req_item.set_save_account_info_by_key_response(was_successful=False,
                                                           failure_reason="Unable to validate password")
