from __future__ import annotations

from typing import List

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor, \
    CursorBase, MySQLCursorBuffered, MySQLCursorRaw, MySQLCursorBufferedRaw, \
    MySQLCursorDict, MySQLCursorBufferedDict, MySQLCursorNamedTuple, MySQLCursorBufferedNamedTuple, MySQLCursorPrepared

from database.db import QueryBuilder, DBContext, DBContextManager, DBTransaction, DBRollbackError, DBCommitError, \
    DBQueryError, DB
from global_logger import *


class MySQLQueryBuilder(QueryBuilder):
    """This class holds all the mysql syntax for the sql class"""

    def __init__(self):
        self.table_name = 'test'

    def get_password_for(self, username) -> str:
        select_statement = "SELECT password FROM user WHERE username ='" + \
                           username + "';"
        return select_statement

    def change_password(self, username, password) -> str:
        query = "UPDATE user SET password = '" + str(password) + "' WHERE username = '" + str(username) + "';"
        return query

    def validate_user_exists(self, username) -> str:
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

    def check_if_friend_request_exists(self, user_id, friends_id) -> str:
        query = "SELECT EXISTS(SELECT user_id FROM friend_list WHERE user_id = \
        " + str(user_id) + " AND friend_id = " + str(friends_id) + " AND request_accepted = 0);"
        return query

    def validate_username_available(self, username) -> str:
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

    def get_last_user_id(self) -> str:
        return "SELECT MAX(user_id) FROM user;"

    def create_user(self, user_id, parsed_data) -> str:
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        user_id = str(user_id)
        username = parsed_data["username"]
        first_name = parsed_data["first_name"]
        last_name = parsed_data["last_name"]
        email = parsed_data["email"]
        password = parsed_data["password"]
        sql_statement = f"INSERT INTO user VALUES({user_id},'{username}','{first_name}','{last_name}','{email}',0,\
        '{password}',null,'{now}',1,1,1,1,False,True,1);"
        return sql_statement

    # id, username, firstname, lastname, email, avatar, ####, password, now, signon_token,

    def create_user_stats(self, user_id) -> str:
        return "INSERT INTO user_statistics VALUES(" + str(user_id) + ",0,0,0,0,0,null,1);"

    def get_friends_list(self, user_id) -> str:
        query = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(user_id) + \
                " AND request_accepted = 1;"
        return query

    def get_user_id(self, username) -> str:
        query = "SELECT user_id FROM user WHERE username = '" + username + "';"
        return query

    def get_user_from_id(self, user_id) -> str:
        query = "SELECT username FROM user WHERE user_id = '" + str(user_id) + "';"
        return query

    def get_user_stats(self, user_id) -> str:
        query = "SELECT * FROM user_statistics WHERE user_id = " + user_id + ";"
        return query

    def signin(self, username, token, token_expiration) -> str:
        query = "UPDATE user SET token_creation='" + token_expiration + \
                "',signon_token='" + token + "' WHERE username = " + \
                "'" + username + "';"
        return query

    def get_token(self, username) -> str:
        query = "SELECT signon_token FROM user WHERE username='" + username + "';"
        return query

    def get_token_creation_time(self, username) -> str:
        query = "SELECT unix_timestamp(token_creation) FROM user WHERE username='" + username + "';"
        return query

    def send_friend_request(self, user_id, friend_id) -> str:
        query = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                "," + str(friend_id) + ",0);"
        return query

    def add_friend(self, user_id, friend_id) -> str:
        query = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                "," + str(friend_id) + ",1);"
        return query

    # UserId and friend_id are backwards... that is intentional

    def accept_friend_request(self, user_id, friend_id, accepted_request) -> str:
        query = "UPDATE friend_list set request_accepted = " + str(accepted_request) + \
                " WHERE friend_id = " + str(user_id) + " AND user_id = " + \
                str(friend_id) + ";"
        return query

    def remove_friend(self, user_id, friend_id) -> str:
        query = "DELETE FROM friend_list WHERE user_id = " + str(user_id) + " AND friend_id = " + str(friend_id) + ";"
        return query

    def check_for_friend_requests(self, user_id) -> str:
        query = f'SELECT user.user_id, user.username FROM user \
        INNER JOIN friend_list ON user.user_id = friend_list.user_id WHERE friend_list.friend_id = {str(user_id)} \
        AND request_accepted = 0;'
        return query

    #  FIXME Remove noinspection comment when implemented
    # noinspection PyUnreachableCode,PyUnusedLocal

    def revoke_friend_request(self, user_id, friend_id) -> str:
        raise NotImplementedError('revoke_friend_request has not been implemented yet')  # FIXME remove when implemented
        query = f'SELECT friend_list.user_id, '

        return query

    def logout(self, username) -> str:
        query = f"UPDATE user SET signon_token = null WHERE username = '{username}';"
        return query

    def get_most_games_won(self, number_of_games) -> str:
        query = "select user.username, user_statistics.* from user inner join user_statistics on user.user_id = \
        user_statistics.user_id order by games_won desc limit " + str(
            number_of_games) + ";"
        return query

    def get_longest_win_streak(self, number_of_games) -> str:
        query = "select user.username, user_statistics.* from user \
        inner join user_statistics on user.user_id = user_statistics.user_id\
        order by longest_win_streak desc limit" + str(number_of_games) + ";"
        return query

    def get_account_info(self, username) -> str:
        query = "SELECT user.avatar, user.chess_board_style,  user.chess_piece_style, \
        user.match_clock_choice, user.automatic_queueing, user.disable_pausing, user.require_commit_press, \
        user_statistics.level FROM user inner join user_statistics on user.user_id = user_statistics.user_id \
        Where username = '" + str(username) + "';"
        return query

    def save_account_info(self, username, data) -> str:
        query = "UPDATE user, user_statistics SET user.avatar = " + str(
            data["avatar_style"]) + ", user.chess_board_style = " + str(
            data["chess_board_style"]) + ", user.chess_piece_style = " + str(data["chess_piece_style"]) + \
                ", user.match_clock_choice =  " + str(
            data["match_clock_choice"]) + ", user.automatic_queueing = " + str(
            data["automatic_queueing"]) + ", user.disable_pausing = " + str(data["disable_pausing"]) + \
                ", user.require_commit_press =  " + str(
            data["require_commit_press"]) + ", user_statistics.level = " + str(
            data["level"]) + " WHERE user.username = '" + str(username) + "';"
        return query

    def save_account_info_by_key(self, username, key, value) -> Optional[str]:
        column = self.get_column(key)
        if (column is None):
            return None
        query = "UPDATE user, user_statistics SET " + str(column) + " = " + str(
            value) + " WHERE user.username = '" + str(username) + "';"
        return query

    def get_column(self, key) -> str:
        # noinspection SpellCheckingInspection
        columns = {
            # key : column
            "avatar_style": "user.avatar",
            "chessboard_style": "user.chess_board_style",
            "chesspiece_style": "user.chess_piece_style",
            "match_clock_choice": "user.match_clock_choice",
            "automatic_queueing": "user.automatic_queueing",
            "disable_pausing": "user.disable_pausing",
            "require_commit_press": "user.require_commit_press",
            "level": "user_statistics.level"
        }
        return columns.get(key)

    @classmethod
    def db_check(cls):
        return "SELECT user_id FROM user;"


class MySQLContext(DBContext):
    def __init__(self):
        self._fetched: List[tuple] = []
        self._db_connection: MySQLConnection = None
        self._transactions: List[DBTransaction] = []
        self._cursor = None

    @property
    def fetched(self) -> List[tuple]:
        return self._fetched

    @property
    def db_connection(self) -> MySQLConnection:
        return self._db_connection

    @logged_method
    @db_connection.setter
    def db_connection(self, connection: MySQLConnection):
        self._db_connection = connection
        self._cursor = connection.cursor()
        logger.debug(f'cursor set to {self._cursor}')

    @property
    def cursor(self) -> Union[CursorBase,
                              MySQLCursor,
                              MySQLCursorBuffered,
                              MySQLCursorRaw,
                              MySQLCursorBufferedRaw,
                              MySQLCursorDict,
                              MySQLCursorBufferedDict,
                              MySQLCursorNamedTuple,
                              MySQLCursorBufferedNamedTuple,
                              MySQLCursorPrepared]:
        # noinspection PyTypeChecker
        return self._cursor

    @property
    def was_successful(self) -> bool:
        """True if all transactions have been committed successfully."""
        return all(t.was_committed for t in self._transactions)

    @property
    def transactions(self) -> List[DBTransaction]:
        """A list of transactions."""
        return self._transactions

    def execute(self, statement: str):
        """Execute given statement on the database."""
        if not self._transactions or self._transactions[-1].is_closed:
            self._transactions.append(DBTransaction())
        self._transactions[-1].add_statement(statement)
        try:
            return self.cursor.execute(statement)
        except mysql.connector.Error as e:
            self.db_connection.rollback()
            self.transactions[-1].was_rolled_back = True
            raise DBQueryError(statement, f"error in sql statement: {statement}") from e

    def commit(self) -> None:
        """Commits the current transaction."""
        if not self._transactions or not self._transactions[-1].statements:
            raise DBCommitError(self._transactions[-1], 'Nothing to commit')
        if self._transactions[-1].is_closed:
            raise DBCommitError(self._transactions[-1], 'Transaction already closed')
        try:
            self.db_connection.commit()
            self.transactions[-1].was_committed = True
        except mysql.connector.Error as e:
            self.db_connection.rollback()
            self.transactions[-1].was_rolled_back = True
            raise DBCommitError(self._transactions[-1], f"Failed to commit database transaction.") from e

    def rollback(self) -> None:
        """Rolls back the current transaction."""
        if not self._transactions or not self._transactions[-1].statements:
            raise DBRollbackError(self._transactions[-1], 'Nothing to rollback')
        if self._transactions[-1].is_closed:
            raise DBRollbackError(self._transactions[-1], 'Transaction already closed')

        self.db_connection.rollback()
        self.transactions[-1].was_rolled_back = True

    def fetchall(self) -> List[tuple]:
        """Gets all rows of a query result, stores them in the context field `fetched` and also returned."""
        self._fetched = self.cursor.fetchall()
        return self.fetched


class MySQLContextManager(DBContextManager):
    def __init__(self,
                 user,
                 password,
                 host,
                 database,
                 auth_plugin):
        self._auth_plugin = auth_plugin
        self._database = database
        self._host = host
        self._password = password
        self._user = user
        self._context = None

    @property
    def auth_plugin(self):
        return self._auth_plugin

    @property
    def database_name(self) -> str:
        return self._database

    @property
    def host(self) -> str:
        return self._host

    @property
    def password(self) -> str:
        return self._password

    @property
    def user(self) -> str:
        return self._user

    @property
    def context(self) -> MySQLContext:
        return self._context

    @logged_method
    def __enter__(self) -> MySQLContext:
        self._context = MySQLContext()
        self._context.db_connection = mysql.connector.connect(user=self.user, password=self.password,
                                                              host=self.host,
                                                              database=self.database_name,
                                                              auth_plugin=self.auth_plugin)
        log(f'cursor is {self._context.cursor}')
        return self._context

    # noinspection PyBroadException
    @logged_method()
    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_val:
            log_error(exc_val)
            self.context.result = False
        else:
            self.context.result = True

        try:
            if self.context.cursor:
                self.context.cursor.close()
        except BaseException as e0:
            log_error(e0)
        try:
            if self.context.db_connection:
                self.context.db_connection.close()
        except BaseException as e1:
            log_error(e1)

        return self.context.result


class MySQLDB(DB):
    def __init__(self, user, password, reader, writer, database: str):
        """ Initializes the DB object.

        Args:
            user: The user accessing the database.
            password: The password used to access database.
            reader: TODO
            writer: TODO
            database: The name of the database being accessed.

        Raises:
            CouldNotConnectException: If connection test fails.
        """
        self.user = user
        self.password = password
        self.reader = reader
        self.writer = writer
        self.database = database
        self.auth_plugin = 'mysql_native_password'

        def mysql_context_manager_factory():
            return MySQLContextManager(user=self.user,
                                       password=self.password,
                                       host=self.writer,
                                       database=self.database,
                                       auth_plugin=self.auth_plugin)

        super().__init__(MySQLQueryBuilder(), mysql_context_manager_factory)
