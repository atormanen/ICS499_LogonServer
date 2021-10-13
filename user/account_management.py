# Is this class nececary? Should it be combined with signin?
from user.tokens import Tokens
import time
from global_logger import logger, VERBOSE
import inspect


class AccountManagement:
    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    username = ''
    password = ''

    def __init__(self, mysqlDB):
        self.db = mysqlDB

    def validateUsername(self, username):
        self.log_function_name()
        if (self.db.validateUserExists(username)):
            return True
        return False

    def isPasswordValid(self, password):
        self.log_function_name()
        upper_ctr, lower_ctr, number_ctr, special_ctr = 0, 0, 0, 0
        for i in range(len(str)):
            if str[i] >= 'A' and str[i] <= 'Z':
                upper_ctr += 1
            elif str[i] >= 'a' and str[i] <= 'z':
                lower_ctr += 1
            elif str[i] >= '0' and str[i] <= '9':
                number_ctr += 1
            else:
                special_ctr += 1
        numberOfGoodChar = upper_ctr + number_ctr + special_ctr

        if (numberOfGoodChar >= 3):
            return True
        else:
            return False

    def createAccount(self, reqItem):
        parsed_data = reqItem.parsed_data
        self.log_function_name()
        # check if username exists
        result = self.db.validateUsernameAvailable(parsed_data["username"])

        # call mysqlDB to create CreateAccount
        if result == 0:
            self.db.createUser(parsed_data)
            reqItem.set_create_account_response(True)
        else:
            reqItem.set_create_account_response(False, 'username already exists')

    def getUserStats(self, parsed_data, reqItem):
        self.log_function_name()
        stats = self.db.getUserStats(parsed_data["username"])
        reqItem.set_get_user_stats_response(stats[0])

    def validatePassword(self, username, password):
        self.log_function_name()
        if (self.db.validateUserExists(username)):
            dbPassword = self.db.getPasswordFor(username)
            dbPassword = dbPassword[0][0]
            # compare password to given getPassword
            if (password == dbPassword):
                return True
        return False

    def tokenUpToDate(self, username):
        self.log_function_name()
        tokenExpiration = self.db.getTokenCreationTime(username)
        # if(tokenExpiration):
        #    return False
        currentTime = time.time()
        timeDiference = currentTime - tokenExpiration[0][0]
        if (timeDiference > 86400):
            return False
        return True

    def changePassword(self, parsed_data, reqItem):
        self.log_function_name()
        username = parsed_data["username"]
        # signonToken = parsed_data["signon_token"]
        oldPassword = parsed_data["old_password"]
        newPassword = parsed_data["new_password"]
        if self.validatePassword(username, oldPassword):
            # TODO remove commented out code if it is not needed
            # if(True):
            savedPassword = self.db.getPasswordFor(username)
            savedPassword = savedPassword[0][0]

            if (savedPassword == oldPassword):
                self.db.changePassword(username, newPassword)
                reqItem.set_change_password_response(was_successful=True)
            else:
                reqItem.set_change_password_response(was_successful=False,
                                                     failure_reason='Provided previous password was not a match')
        # else:
        #     print("token is not up to date")
        #     reqItem.set_change_password_response("fail")
        else:
            reqItem.set_change_password_response(was_successful=False,
                                                 failure_reason='Unable to validate password.')

    def saveAccountInfoByKey(self, parsed_data, reqItem):
        self.log_function_name()
        username = parsed_data["username"]
        signonToken = parsed_data["signonToken"]
        hash = parsed_data["hash"]
        key = parsed_data["key"]
        value = parsed_data["value"]
        type = parsed_data["type"]
        if (self.validatePassword(username, hash)):
            self.db.saveAccountInfoByKey(username, key, value)
            reqItem.set_save_account_info_by_key_response(was_successful=True)
        else:
            reqItem.set_save_account_info_by_key_response(was_successful=False,
                                                          failure_reason="Unable to validate password")
