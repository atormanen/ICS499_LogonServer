from typing import Optional, List

import mysql.connector

from database.mysql_db import MysqlDB
from global_logger import logger, logged_method


# from query_builder import query_builder

# MysqlDB is a class used to implement common database queries programmatically. It
# uses the query_builder class which holds the actual mysql syntax.

class _DBContext:
    def __init__(self):
        self.fetched: List[tuple] = []
        self.db = None
        self.cursor = None
        self.result: Optional[bool] = None
        self.statements = []

    def execute(self, statement):
        """Execute given statement on the database."""
        self.statements.append(statement)
        try:
            return_value = self.cursor.execute(statement)
        except Exception as e:
            logger.debug(f"error in sql statement: {self.statements[-1]}")
            raise e
        return return_value

    def commit(self) -> None:
        """Commits the current transaction."""
        self.db.commit()

    def fetchall(self) -> List[tuple]:
        """Gets all rows of a query result, stores them in the context field `fetched` and also returned."""
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


class FailureException(Exception):
    """An exception raised to give more information about the failure."""

    def __init__(self, msg: str, *args):
        super().__init__(msg, *args)
        self._msg: str = msg

    @property
    def failure_reason_msg(self) -> str:
        """The exception's message."""
        return self._msg


class UserNotFoundException(FailureException):
    """An exception to be raised if a user cannot be found."""

    def __init__(self, username: str):
        """ Creates an instance of this exception.

        :param username: The username of the user that could not be found.
        """
        super().__init__(f'user with username {username!r} was not found.')


class FriendRequestNotFoundException(FailureException):
    """An exception to be raised if a friend request cannot be found."""

    def __init__(self, username, friend_username):
        super().__init__(f'No friend request found from {friend_username} on {username}\'s list.')


class DB:

    def __init__(self, user, password, reader, writer, database: MysqlDB):
        self.builder = MysqlDB()
        self.user = user
        self.password = password
        self.reader = reader
        self.writer = writer
        self.database = database

    @logged_method
    def db_insert(self, statement: str) -> bool:

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return False if c.result is None else c.result

    @logged_method
    def db_fetch(self, statement: str) -> List[tuple]:

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.fetchall()
        return c.fetched

    @logged_method
    def db_update(self, statement: str) -> bool:
        """Updates the database.

        :param statement: The query that will be executed.
        :return: True if successful, else False.
        """

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return bool(c.result)

    @logged_method
    def db_delete(self, statement: str) -> bool:

        with _DBContextManager(user=self.user, password=self.password, host=self.writer, database=self.database,
                               auth_plugin='mysql_native_password') as c:
            c.execute(statement)
            c.commit()
        return bool(c.result)

    @logged_method
    def get_password_for(self, username: str) -> List[tuple]:
        result = self.db_fetch(self.builder.get_password_for(username))

        # TODO we may want to consider actually returning the password rather than the list.
        return result

    @logged_method
    def increment_signin_failed(self):
        return False  # FIXME

    @logged_method
    def change_password(self, username, password) -> bool:
        status = self.db_update(self.builder.change_password(username, password))
        return status

    @logged_method
    def user_exists(self, username: str) -> bool:
        """Checks if user exists.

        :param username: The username of the user to check for.
        :return: True if the user exists, else False.
        """

        statement = self.builder.validate_user_exists(username)
        result = self.db_fetch(statement)
        result = result[0][0]
        return bool(result)

    @logged_method
    def username_is_available(self, username: str) -> bool:
        """Checks if username is available.

        :param username: The username to check.
        :return: True if the username is available, else False/
        """
        statement = self.builder.validate_username_available(username)
        result = self.db_fetch(statement)
        int_result = result[0][0]
        return bool(int_result)

    @logged_method
    def check_if_friend_request_exists(self, sender_username: str, recipient_username: str) -> bool:
        """ Checks if the a friend request from a particular user to another exists.

        :param sender_username: The username of the user that sent the friend request.
        :param recipient_username: The username of the user receiving the friend request.
        :return: True if the request exists, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(sender_username))
        friends_id = self.db_fetch(self.builder.get_user_id(recipient_username))
        if (user_id is False):
            raise UserNotFoundException(sender_username)
        if (friends_id is False):
            raise UserNotFoundException(recipient_username)
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_fetch(self.builder.check_if_friend_request_exists(user_id, friends_id))
        logger.debug(type(result))
        int_result = result[0][0]
        return bool(int_result)

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
    def signin(self, username: str, token, token_creation_time) -> bool:
        """

        :param username: The username that is to be signed in.
        :param token: TODO add a type hint and describe what this argument represents.
        :param token_creation_time: TODO add a type hint and describe what the this argument represents.
        :return:
        """
        result = self.db_update(self.builder.signin(username, token, token_creation_time))
        return result

    @logged_method
    def get_token(self, username):
        result = self.db_fetch(self.builder.get_token(username))

        # TODO we may want to think about extracting the needed token and returning that in
        #  a way that is easier to use. The parsing of database results should be the responsibility
        #  of the db module, not the caller.

        return result

    @logged_method
    def get_token_creation_time(self, username: str) -> List[tuple]:
        """Gets the token creation time.

        :param username: The username of the user who's token creation time we are retrieving.
        :return: TODO describe what to expect as a result with enough detail to use it
        """
        result = self.db_fetch(self.builder.get_token_creation_time(username))

        # TODO we may want to think about extracting the needed time and returning that in
        #  a way that is easier to use. The parsing of database results should be the responsibility
        #  of the db module, not the caller.

        return result

    @logged_method
    def get_friends_list(self, username: str) -> List[tuple]:
        """Gets the friends list of a target user

        :param username: The username of the user who's friends list will be returned.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        result = self.db_fetch(self.builder.get_friends_list(user_id[0][0]))

        # FIXME We may want to consider making a FriendsList class and return one of those
        #  objects rather than putting the burden of parsing this database result onto the
        #  caller.

        return result

    @logged_method
    def get_user_stats(self, username: str) -> List[tuple]:
        """Gets the user statistics.

        :param username: the username of the user who's statistics will be retrieved.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        user_id = str(user_id[0][0])
        result = self.db_fetch(self.builder.get_user_stats(user_id))

        # FIXME We may want to consider making a UserStats class and return one of those
        #  objects rather than putting the burden of parsing this database result onto
        #  the caller.

        return result

    @logged_method
    def send_friend_request(self, username: str, friends_username: str) -> bool:
        """Sends a friend request to the target friend.

        :param username: The username of the sender.
        :param friends_username: The username of the target.
        :return: True if successful, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            raise UserNotFoundException(username)
        if (friends_id is False):
            raise UserNotFoundException(friends_username)
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_insert(self.builder.send_friend_request(user_id, friends_id))
        return result

    @logged_method
    def accept_friend_request(self, username: str, friends_username: str, accepted_request: bool) -> bool:
        """Accepts a friend request.

        :param username: The username of the user accepting the request.
        :param friends_username: The friend that sent the request.
        :param accepted_request: True if accepting, else False.
        :return: True if successful, else False.
        :raises FriendRequestNotFoundException If a request cannot be found in the database matching the sender and
        receiver.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if not self.check_if_friend_request_exists(friends_username, username):
            # we don't need to check if username or friend_username correspond to existing
            # accounts because that happens in the check_if_friend_request_exists call.
            # That said, we should keep in mind that this can raise a UserNotFoundException
            raise FriendRequestNotFoundException(username, friends_username)

        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        result = self.db_update(self.builder.accept_friend_request(user_id, friends_id, accepted_request))
        self.db_update(self.builder.add_friend(user_id, friends_id))
        return result

    @logged_method
    def remove_friend(self, username: str, friends_username: str) -> None:
        """Removes a particular friend from a users friends list.

        :param username: The username of the user who is removing a friend.
        :param friends_username: The username of the friend to be removed.
        :return: True if successful, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        friends_id = self.db_fetch(self.builder.get_user_id(friends_username))
        if (user_id is False):
            raise UserNotFoundException(username)
        if (friends_id is False):
            raise UserNotFoundException(friends_username)
        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        was_successful = self.db_delete(self.builder.remove_friend(user_id, friends_id))
        self.db_delete(self.builder.remove_friend(friends_id, user_id))
        if not was_successful:
            raise FailureException(f'request to remove {friends_username} from {username}\'s '
                                   f'friend list failed for unknown reasons.')

    @logged_method
    def check_for_friend_requests(self, username: str) -> List[tuple]:
        """Checks for friend requests for a particular user.

        :param username: The username of the user for whom to check friend requests.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        user_id = user_id[0][0]
        result = self.db_fetch(self.builder.check_for_friend_requests(user_id))

        # FIXME We may want to consider making a FriendRequest class and return one of
        #  those rather than putting the burden of parsing this database result onto the
        #  caller.

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
    def save_account_info_by_key(self, username, key, value) -> None:
        query = self.builder.save_account_info_by_key(username, key, value)
        if (query is None):
            return
        else:
            self.db_update(query)
