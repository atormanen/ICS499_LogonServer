from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Callable, Optional
from global_logger import log


class DatabaseFailureException(Exception):
    """An exception raised to give more information about the failure."""

    def __init__(self, msg: str, *args):
        super().__init__(msg, *args)
        self._msg: str = msg

    @property
    def failure_reason_msg(self) -> str:
        """The exception's message."""
        return self._msg


class TransactionClosedException(DatabaseFailureException):
    """An exception that is raised if trying to perform illegal operations on a closed transaction"""

    def __init__(self, *args):
        super().__init__(*args)


class DBQueryError(DatabaseFailureException):
    """An exception that is raised if a database query failed."""

    def __init__(self, query, *args):
        super().__init__(*args)


class DBCommitError(DatabaseFailureException):
    """An exception that is raised if a commit fails."""

    def __init__(self, transaction, *args):
        super().__init__(*args)


class DBRollbackError(DatabaseFailureException):
    """An exception that is raised if a rollback fails."""

    def __init__(self, transaction, *args):
        super().__init__(*args)


class CouldNotConnectException(DatabaseFailureException):
    """An exception that is raised if a database connection check fails"""

    def __init__(self):
        super().__init__('Could not connect to database')


class UserNotFoundException(DatabaseFailureException):
    """An exception to be raised if a user cannot be found."""

    def __init__(self, username: str):
        """ Creates an instance of this exception.

        :param username: The username of the user that could not be found.
        """
        super().__init__(f'user with username {username!r} was not found.')


class FriendRequestNotFoundException(DatabaseFailureException):
    """An exception to be raised if a friend request cannot be found."""

    def __init__(self, username, friend_username):
        super().__init__(f'No friend request found from {friend_username} on {username}\'s list.')


@dataclass
class DBTransaction:
    statements: list[str] = field(default_factory=list)
    was_committed: bool = False
    was_rolled_back: bool = False

    def add_statement(self, statement: str) -> None:
        if self.was_committed:
            raise TransactionClosedException("Cannot add a statement to a transaction that has been committed")

        if self.was_rolled_back:
            raise TransactionClosedException("Cannot add a statement to a transaction that has been rolled back")

        self.statements.append(statement)

    @property
    def is_closed(self):
        return self.was_committed or self.was_rolled_back


class DBContext(ABC):

    @property
    @abstractmethod
    def fetched(self) -> List[tuple]:
        """Any fetched Data."""
        ...

    @property
    @abstractmethod
    def was_successful(self) -> bool:
        """True if the transaction was committed successfully."""
        ...

    @abstractmethod
    def execute(self, statement) -> None:
        """Execute given statement on the database."""
        ...

    @abstractmethod
    def commit(self) -> None:
        """Commits the current transaction."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Commits the current transaction."""
        ...

    @abstractmethod
    def fetchall(self) -> List[tuple]:
        """Gets all rows of a query result, stores them in the context field `fetched` and also returned."""
        ...


class DBContextManager(ABC):

    @abstractmethod
    def __enter__(self) -> DBContext: ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool: ...


class QueryBuilder(ABC):

    @abstractmethod
    def get_password_for(self, username) -> str: ...

    @abstractmethod
    def change_password(self, username, password) -> str: ...

    @abstractmethod
    def validate_user_exists(self, username) -> str: ...

    @abstractmethod
    def check_if_friend_request_exists(self, user_id, friends_id) -> str: ...

    @abstractmethod
    def validate_username_available(self, username) -> str: ...

    @abstractmethod
    def get_last_user_id(self) -> str: ...

    @abstractmethod
    def create_user(self, user_id, parsed_data) -> str: ...

    @abstractmethod
    def create_user_stats(self, user_id) -> str: ...

    @abstractmethod
    def get_friends_list(self, user_id) -> str: ...

    @abstractmethod
    def get_user_id(self, username) -> str: ...

    @abstractmethod
    def get_user_from_id(self, user_id) -> str: ...

    @abstractmethod
    def get_user_stats(self, user_id) -> str: ...

    @abstractmethod
    def signin(self, username, token, token_expiration) -> str: ...

    @abstractmethod
    def get_token(self, username) -> str: ...

    @abstractmethod
    def get_token_creation_time(self, username) -> str: ...

    @abstractmethod
    def send_friend_request(self, user_id, friend_id) -> str: ...

    @abstractmethod
    def add_friend(self, user_id, friend_id) -> str: ...

    @abstractmethod
    def accept_friend_request(self, user_id, friend_id, accepted_request) -> str: ...

    @abstractmethod
    def remove_friend(self, user_id, friend_id) -> str: ...

    @abstractmethod
    def check_for_friend_requests(self, user_id) -> str: ...

    @abstractmethod
    def revoke_friend_request(self, user_id, friend_id) -> str: ...

    @abstractmethod
    def logout(self, username) -> str: ...

    @abstractmethod
    def get_most_games_won(self, number_of_games) -> str: ...

    @abstractmethod
    def get_longest_win_streak(self, number_of_games) -> str: ...

    @abstractmethod
    def get_account_info(self, username) -> str: ...

    @abstractmethod
    def save_account_info(self, username, data) -> str: ...

    @abstractmethod
    def save_account_info_by_key(self, username, key, value) -> Optional[str]: ...

    @abstractmethod
    def get_column(self, key) -> str: ...

    @classmethod
    @abstractmethod
    def db_check(cls) -> str: ...


class DB:

    def __init__(self, query_builder: QueryBuilder, context_manager_factory: Callable):
        """ Initializes the DB object.

        Raises:
            CouldNotConnectException: If connection test fails.
        """
        self.query_builder = query_builder
        self.context_manager_factory: Callable = context_manager_factory

        # check to see that connection is good... if not the caller wants to know asap
        self._test_db_connection()  # this raises CouldNotConnectException if connection fails

    def db_insert(self, statement: str) -> bool:

        with self.context_manager_factory() as c:
            c.execute(statement)
            c.commit()
        return False if c.result is None else c.result

    def db_fetch(self, statement: str) -> List[tuple]:
        with self.context_manager_factory() as c:
            c.execute(statement)
            c.fetchall()
        return c.fetched

    def db_update(self, statement: str) -> bool:
        """Updates the database.

        :param statement: The query that will be executed.
        :return: True if successful, else False.
        """

        with self.context_manager_factory() as c:
            c.execute(statement)
            c.commit()
        return bool(c.result)

    # @logged_method
    def db_delete(self, statement: str) -> bool:

        with self.context_manager_factory() as c:
            c.execute(statement)
            c.commit()
        return bool(c.result)

    # @logged_method
    def get_password_for(self, username: str) -> List[tuple]:
        result = self.db_fetch(self.query_builder.get_password_for(username))

        # TODO we may want to consider actually returning the password rather than the list.
        return result

    # @logged_method
    def increment_signin_failed(self):
        return False  # FIXME

    # @logged_method
    def change_password(self, username, password) -> bool:
        status = self.db_update(self.query_builder.change_password(username, password))
        return status

    # @logged_method
    def user_exists(self, username: str) -> bool:
        """Checks if user exists.

        :param username: The username of the user to check for.
        :return: True if the user exists, else False.
        """

        statement = self.query_builder.validate_user_exists(username)
        result = self.db_fetch(statement)
        result = result[0][0]
        return bool(result)

    # @logged_method
    def username_is_available(self, username: str) -> bool:
        """Checks if username is available.

        :param username: The username to check.
        :return: True if the username is available, else False/
        """
        statement = self.query_builder.validate_username_available(username)
        result = self.db_fetch(statement)
        int_result = result[0][0]
        return bool(int_result)

    # @logged_method
    def check_if_friend_request_exists(self, sender_username: str, recipient_username: str) -> bool:
        """ Checks if the a friend request from a particular user to another exists.

        :param sender_username: The username of the user that sent the friend request.
        :param recipient_username: The username of the user receiving the friend request.
        :return: True if the request exists, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.query_builder.get_user_id(sender_username))
        friends_id = self.db_fetch(self.query_builder.get_user_id(recipient_username))
        if (user_id is False):
            raise UserNotFoundException(sender_username)
        if (friends_id is False):
            raise UserNotFoundException(recipient_username)
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_fetch(self.query_builder.check_if_friend_request_exists(user_id, friends_id))
        log(f'type of result from check_if_friend_request_exists: {type(result)}')
        int_result = result[0][0]
        return bool(int_result)

    # @logged_method
    def create_user(self, parsed_data):
        user_id = self.db_fetch(self.query_builder.get_last_user_id())
        user_id = user_id[0][0]
        if (user_id is None):
            user_id = 1
        else:
            if isinstance(user_id, str):
                user_id = eval(user_id)
            user_id = str(user_id + 1)
        statement = self.query_builder.create_user(user_id, parsed_data)
        self.db_insert(statement)
        result = self.db_insert(self.query_builder.create_user_stats(user_id))
        return result

    # @logged_method
    def signin(self, username: str, token, token_creation_time) -> bool:
        """

        :param username: The username that is to be signed in.
        :param token: TODO add a type hint and describe what this argument represents.
        :param token_creation_time: TODO add a type hint and describe what the this argument represents.
        :return:
        """
        result = self.db_update(self.query_builder.signin(username, token, token_creation_time))
        return result

    # @logged_method
    def get_token(self, username: str):
        result = self.db_fetch(self.query_builder.get_token(username))

        # TODO we may want to think about extracting the needed token and returning that in
        #  a way that is easier to use. The parsing of database results should be the responsibility
        #  of the db_connection module, not the caller.

        return result

    # @logged_method
    def get_token_creation_time(self, username: str) -> List[tuple]:
        """Gets the token creation time.

        :param username: The username of the user who's token creation time we are retrieving.
        :return: TODO describe what to expect as a result with enough detail to use it
        """
        result = self.db_fetch(self.query_builder.get_token_creation_time(username))

        # TODO we may want to think about extracting the needed time and returning that in
        #  a way that is easier to use. The parsing of database results should be the responsibility
        #  of the db_connection module, not the caller.

        return result

    # @logged_method
    def get_friends_list(self, username: str) -> List[tuple]:
        """Gets the friends list of a target user

        :param username: The username of the user who's friends list will be returned.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        result = self.db_fetch(self.query_builder.get_friends_list(user_id[0][0]))

        # FIXME We may want to consider making a FriendsList class and return one of those
        #  objects rather than putting the burden of parsing this database result onto the
        #  caller.

        return result

    # @logged_method
    def get_user_stats(self, username: str) -> List[tuple]:
        """Gets the user statistics.

        :param username: the username of the user who's statistics will be retrieved.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        user_id = str(user_id[0][0])
        result = self.db_fetch(self.query_builder.get_user_stats(user_id))

        # FIXME We may want to consider making a UserStats class and return one of those
        #  objects rather than putting the burden of parsing this database result onto
        #  the caller.

        return result

    # @logged_method
    def send_friend_request(self, username: str, friends_username: str) -> bool:
        """Sends a friend request to the target friend.

        :param username: The username of the sender.
        :param friends_username: The username of the target.
        :return: True if successful, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """
        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        friends_id = self.db_fetch(self.query_builder.get_user_id(friends_username))
        if (user_id is False):
            raise UserNotFoundException(username)
        if (friends_id is False):
            raise UserNotFoundException(friends_username)
        user_id = user_id[0][0]
        friends_id = friends_id[0][0]
        result = self.db_insert(self.query_builder.send_friend_request(user_id, friends_id))
        return result

    # @logged_method
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
        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        friends_id = self.db_fetch(self.query_builder.get_user_id(friends_username))
        if not self.check_if_friend_request_exists(friends_username, username):
            # we don't need to check if username or friend_username correspond to existing
            # accounts because that happens in the check_if_friend_request_exists call.
            # That said, we should keep in mind that this can raise a UserNotFoundException
            raise FriendRequestNotFoundException(username, friends_username)

        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        result = self.db_update(self.query_builder.accept_friend_request(user_id, friends_id, accepted_request))
        self.db_update(self.query_builder.add_friend(user_id, friends_id))
        return result

    # @logged_method
    def remove_friend(self, username: str, friends_username: str) -> None:
        """Removes a particular friend from a users friends list.

        :param username: The username of the user who is removing a friend.
        :param friends_username: The username of the friend to be removed.
        :return: True if successful, else False.
        :raises UserNotFoundException If either user cannot be found in the database.
        """

        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        friends_id = self.db_fetch(self.query_builder.get_user_id(friends_username))
        if (user_id is False):
            raise UserNotFoundException(username)
        if (friends_id is False):
            raise UserNotFoundException(friends_username)
        friends_id = friends_id[0][0]
        user_id = user_id[0][0]
        was_successful = self.db_delete(self.query_builder.remove_friend(user_id, friends_id))
        if was_successful:
            was_successful = all([was_successful, bool(self.db_delete(self.query_builder.remove_friend(friends_id, user_id)))])
        if not was_successful:
            raise DatabaseFailureException(f'request to remove {friends_username} from {username}\'s '
                                           f'friend list failed for unknown reasons.')

    # @logged_method
    def check_for_friend_requests(self, username: str) -> List[tuple]:
        """Checks for friend requests for a particular user.

        :param username: The username of the user for whom to check friend requests.
        :return: TODO describe what to expect as a result with enough detail to use it
        :raises UserNotFoundException If the user cannot be found in the database.
        """
        user_id = self.db_fetch(self.query_builder.get_user_id(username))
        if (user_id is False):
            raise UserNotFoundException(username)
        user_id = user_id[0][0]
        result = self.db_fetch(self.query_builder.check_for_friend_requests(user_id))

        # FIXME We may want to consider making a FriendRequest class and return one of
        #  those rather than putting the burden of parsing this database result onto the
        #  caller.

        return result

    # @logged_method
    def logout(self, username: str):
        self.db_update(self.query_builder.logout(username))

    # @logged_method
    def get_most_chess_games_won(self, number_of_games):
        result = self.db_fetch(self.query_builder.get_most_games_won(number_of_games))
        return result

    # @logged_method
    def get_longest_win_streak(self, number_of_games):
        result = self.db_fetch(self.query_builder.get_longest_win_streak(number_of_games))
        return result

    # @logged_method
    def get_account_info(self, username: str):
        result = self.db_fetch(self.query_builder.get_account_info(username))
        return result

    # @logged_method
    def save_account_info(self, username: str, data):
        self.db_update(self.query_builder.save_account_info(username, data))

    def save_account_info_by_key(self, username: str, key, value) -> None:
        query = self.query_builder.save_account_info_by_key(username, key, value)
        if (query is None):
            return
        else:
            self.db_update(query)

    def _test_db_connection(self):
        """tests the database connection.

        Note that this should only be used when initializing the DB object

        Raises:
            CouldNotConnectException: If the test fails to connect.

        """
        try:
            self.db_fetch(self.query_builder.db_check())
        except CouldNotConnectException as e:
            raise e
        except BaseException as e:
            raise CouldNotConnectException from e


