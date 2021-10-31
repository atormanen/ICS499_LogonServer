from typing import Optional, List

import mysql.connector

from database.mysql_db import MysqlDB
from global_logger import logger, logged_method


# from query_builder import query_builder

# MysqlDB is a class used to implement common database queries programmatically. It
# uses the query_builder class which holds the actual mysql syntax.

class _DBContext:
    def __init__(self):
        self.fetched: Optional[List[tuple]] = None
        self.db = None
        self.cursor = None
        self.result: Optional[bool] = None
        self.statements = []

    def execute(self, statement):
        """Execute given statement on the database"""
        self.statements.append(statement)
        try:
            return_value = self.cursor.execute(statement)
        except Exception as e:
            logger.debug(f"error in sql statement: {self.statements[-1]}")
            raise e
        return return_value

    def commit(self) -> None:
        """Commits the current transaction"""
        self.db.commit()

    def fetchall(self) -> List[tuple]:
        """Gets all rows of a query result, stores them in the context field `fetched` and also returned"""
        self.fetched = self.cursor.fetchall()
        return self.fetched


class _DBContextManager:
    def __init__(self,
                 user,
                 password,
                 host,
                 database,
                 auth_plugin):
        self.auth_plugin = auth_plugin
        self.database = database
        self.host = host
        self.password = password
        self.user = user
        self.context = _DBContext()

    def __enter__(self) -> _DBContext:
        self.context.db = mysql.connector.connect(user=self.user, password=self.password,
                                                  host=self.host,
                                                  database=self.database,
                                                  auth_plugin=self.auth_plugin)
        self.context.cursor = self.context.db.cursor()
        return self.context

    # noinspection PyBroadException
    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_val:
            logger.error(exc_val)
            self.context.result = False
        else:
            self.context.result = True

        try:
            if self.context.cursor:
                self.context.cursor.close()
        except BaseException as e0:
            logger.error(e0)
        try:
            if self.context.db:
                self.context.db.close()
        except BaseException as e1:
            logger.error(e1)

        return self.context.result


class DB:

    def __init__(self, user, password, reader, writer, database: MysqlDB):
        self.builder = MysqlDB()
        self.user = user
        self.password = password
        self.reader = reader
        self.writer = writer
        self.database = database

    @logged_method
    def db_insert(self, statement):

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return c.result

        #  TODO delete this if the context manager works out
        # mydb = None
        # cursor = None
        # result = False
        #
        # try:
        #     mydb = mysql.connector.connect(user=self.user, password=self.password,
        #                                    host=self.writer,
        #                                    database=self.database,
        #                                    auth_plugin='mysql_native_password')
        #     cursor = mydb.cursor()
        #     cursor.execute(statement)
        #     mydb.commit()
        #     result = True
        # except mysql.connector.Error as error:
        #     logger.error(error)
        #     logger.debug(f"error in sql statement: {statement}")
        #     result = False
        # finally:
        #     if (mydb.is_connected()):
        #         if cursor:
        #             cursor.close()
        #         if mydb:
        #             mydb.close()
        #     return result

    @logged_method
    def db_fetch(self, statement):

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.fetchall()
        return c.fetched

        #  TODO delete this if the context manager works out
        # mydb = None
        # cursor = None
        # result = False
        # try:
        #     result = ''
        #     mydb = mysql.connector.connect(user=self.user, password=self.password,
        #                                    host=self.reader,
        #                                    database=self.database,
        #                                    auth_plugin='mysql_native_password')
        #     cursor = mydb.cursor()
        #     cursor.execute(statement)
        #     result = cursor.fetchall()
        # except mysql.connector.Error as e:
        #     logger.error(e)
        #     result = None
        # finally:
        #     if (mydb.is_connected()):
        #         cursor.close()
        #         mydb.close()
        #     return result

    @logged_method
    def db_update(self, statement) -> bool:
        """Updates the database

        :param statement: the query that will be executed
        :return: true if successful, else false
        """

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return c.result

        #  TODO delete this if the context manager works out
        # mydb = None
        # cursor = None
        # result = False
        # try:
        #     mydb = mysql.connector.connect(user=self.user, password=self.password,
        #                                    host=self.writer,
        #                                    database=self.database,
        #                                    auth_plugin='mysql_native_password')
        #     cursor = mydb.cursor()
        #     cursor.execute(statement)
        #     mydb.commit()
        #     result = True
        # except mysql.connector.Error as error:
        #     logger.error(error)
        #     result = False
        # finally:
        #     if (mydb.is_connected()):
        #         cursor.close()
        #         mydb.close()
        #     return result

    @logged_method
    def db_delete(self, statement):

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return c.result

        #  TODO delete this if the context manager works out
        # mydb = None
        # cursor = None
        # result = False
        # try:
        #     mydb = mysql.connector.connect(user=self.user, password=self.password,
        #                                    host=self.writer,
        #                                    database=self.database,
        #                                    auth_plugin='mysql_native_password')
        #     cursor = mydb.cursor()
        #     cursor.execute(statement)
        #     mydb.commit()
        #     result = True
        # except mysql.connector.Error as error:
        #     logger.error(error)
        #     result = False
        # finally:
        #     if (mydb.is_connected()):
        #         cursor.close()
        #         mydb.close()
        #     return result

    @logged_method
    def get_password_for(self, username):
        result = self.db_fetch(self.builder.get_password_for(username))
        return result

    @logged_method
    def increment_signin_failed(self):
        return False

    @logged_method
    def change_password(self, username, password):
        status = self.db_update(self.builder.change_password(username, password))
        return status

    # Returns 1\true if exits, false\0 if not
    @logged_method
    def validate_user_exists(self, username):

        statement = self.builder.validate_user_exists(username)
        result = self.db_fetch(statement)
        result = result[0][0]
        return result

    # Returns 1\true if exits, false\0 if not
    @logged_method
    def validate_username_available(self, username):
        statement = self.builder.validate_username_available(username)
        result = self.db_fetch(statement)
        int_result = result[0][0]
        return int_result

    # Returns 1\true if exits, false\0 if not
    @logged_method
    def check_if_friend_request_exists(self, username, friends_username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            return False
        if (friends_id is False):
            return False
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_fetch(self.builder.check_if_friend_request_exists(user_id, friends_id))
        logger.debug(type(result))
        int_result = result[0][0]
        return int_result

    @logged_method
    def create_user(self, parsed_data):
        user_id = self.db_fetch(self.builder.get_last_user_id())
        user_id = user_id[0][0]
        if (user_id is None):
            user_id = 1
        else:
            if isinstance(user_id, str):
                user_id = eval(user_id)
            user_id = str(user_id + 1)
        statement = self.builder.create_user(user_id, parsed_data)
        self.db_insert(statement)
        result = self.db_insert(self.builder.create_user_stats(user_id))
        return result

    @logged_method
    def signin(self, username, token, token_creation_time):
        result = self.db_update(self.builder.signin(username, token, token_creation_time))
        return result

    @logged_method
    def get_token(self, username):
        result = self.db_fetch(self.builder.get_token(username))
        return result

    @logged_method
    def get_token_creation_time(self, username):
        result = self.db_fetch(self.builder.get_token_creation_time(username))
        return result

    @logged_method
    def get_friends_list(self, username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        result = self.db_fetch(self.builder.get_friends_list(user_id[0][0]))
        return result

    @logged_method
    def get_user_info(self, username):
        return False  # FIXME

    @logged_method
    def get_user_stats(self, username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        user_id = str(user_id[0][0])
        result = self.db_fetch(self.builder.get_user_stats(user_id))
        return result

    @logged_method
    def send_friend_request(self, username, friends_username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            return False
        if (friends_id is False):
            return False
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_insert(self.builder.send_friend_request(user_id, friends_id))
        return result

    @logged_method
    def accept_friend_request(self, username, friends_username, accepted_request):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            return False
        if (friends_id is False):
            return False

        # check that the sender and receiver make sense
        friends_friend_requests = self.check_for_friend_requests(friends_username)
        if isinstance(friends_friend_requests, list):
            for request in friends_friend_requests:
                sender = request[0]
                receiver = request[1]
                if sender != friends_username or receiver != username:
                    return False

        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        result = self.db_update(self.builder.accept_friend_request(user_id, friends_id, accepted_request))
        self.db_update(self.builder.add_friend(user_id, friends_id))
        return result

    @logged_method
    def remove_friend(self, username, friends_username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            return False
        if (friends_id is False):
            return False
        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        result = self.db_delete(self.builder.remove_friend(user_id, friends_id))
        self.db_delete(self.builder.remove_friend(friends_id, user_id))
        return result

    @logged_method
    def check_for_friend_requests(self, username):
        user_id = self.db_fetch(self.builder.get_user_id(username))
        if (user_id is False):
            return False
        user_id = user_id[0][0]
        result = self.db_fetch(self.builder.check_for_friend_requests(user_id))
        return result

    @logged_method
    def logout(self, username):
        self.db_update(self.builder.logout(username))

    @logged_method
    def get_most_chess_games_won(self, number_of_games):
        result = self.db_fetch(self.builder.get_most_games_won(number_of_games))
        return result

    @logged_method
    def get_longest_win_streak(self, number_of_games):
        result = self.db_fetch(self.builder.get_longest_win_streak(number_of_games))
        return result

    @logged_method
    def get_account_info(self, username):
        result = self.db_fetch(self.builder.get_account_info(username))
        return result

    @logged_method
    def save_account_info(self, username, data):
        self.db_update(self.builder.save_account_info(username, data))

    @logged_method
    def save_account_info_by_key(self, username, key, value):
        query = self.builder.save_account_info_by_key(username, key, value)
        if (query is None):
            return
        else:
            self.db_update(query)
