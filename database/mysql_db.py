import time
from typing import Optional

from global_logger import logged_method


# TODO: change MysqlDB to db and change query builder to mysql_query
class MysqlDB:
    """This class holds all the mysql syntax for the sql class"""

    def __init__(self):
        self.table_name = 'test'

    @logged_method
    def get_password_for(self, username) -> str:
        select_statement = "SELECT password FROM user WHERE username ='" + \
                           username + "';"
        return select_statement

    @logged_method
    def change_password(self, username, password) -> str:
        query = "UPDATE user SET password = '" + str(password) + "' WHERE username = '" + str(username) + "';"
        return query

    @logged_method
    def validate_user_exists(self, username) -> str:
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

    @logged_method
    def check_if_friend_request_exists(self, user_id, friends_id) -> str:
        query = "SELECT EXISTS(SELECT user_id FROM friend_list WHERE user_id = \
        " + str(user_id) + " AND friend_id = " + str(friends_id) + " AND request_accepted = 0);"
        return query

    @logged_method
    def validate_username_available(self, username) -> str:
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

    @logged_method
    def get_last_user_id(self) -> str:
        return "SELECT MAX(user_id) FROM user;"

    @logged_method
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

    @logged_method
    def create_user_stats(self, user_id) -> str:
        return "INSERT INTO user_statistics VALUES(" + str(user_id) + ",0,0,0,0,0,null,1);"

    @logged_method
    def get_friends_list(self, user_id) -> str:
        query = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(user_id) + \
                " AND request_accepted = 1;"
        return query

    @logged_method
    def get_user_id(self, username) -> str:
        query = "SELECT user_id FROM user WHERE username = '" + username + "';"
        return query

    @logged_method
    def get_user_from_id(self, user_id) -> str:
        query = "SELECT username FROM user WHERE user_id = '" + str(user_id) + "';"
        return query

    @logged_method
    def get_user_stats(self, user_id) -> str:
        query = "SELECT * FROM user_statistics WHERE user_id = " + user_id + ";"
        return query

    @logged_method
    def signin(self, username, token, token_expiration) -> str:
        query = "UPDATE user SET token_creation='" + token_expiration + \
                "',signon_token='" + token + "' WHERE username = " + \
                "'" + username + "';"
        return query

    @logged_method
    def get_token(self, username) -> str:
        query = "SELECT signon_token FROM user WHERE username='" + username + "';"
        return query

    @logged_method
    def get_token_creation_time(self, username) -> str:
        query = "SELECT unix_timestamp(token_creation) FROM user WHERE username='" + username + "';"
        return query

    @logged_method
    def send_friend_request(self, user_id, friend_id) -> str:
        query = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                "," + str(friend_id) + ",0);"
        return query

    @logged_method
    def add_friend(self, user_id, friend_id) -> str:
        query = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                "," + str(friend_id) + ",1);"
        return query

    # UserId and friend_id are backwards... that is intentional
    @logged_method
    def accept_friend_request(self, user_id, friend_id, accepted_request) -> str:
        query = "UPDATE friend_list set request_accepted = " + str(accepted_request) + \
                " WHERE friend_id = " + str(user_id) + " AND user_id = " + \
                str(friend_id) + ";"
        return query

    @logged_method
    def remove_friend(self, user_id, friend_id) -> str:
        query = "DELETE FROM friend_list WHERE user_id = " + str(user_id) + " AND friend_id = " + str(friend_id) + ";"
        return query

    @logged_method
    def check_for_friend_requests(self, user_id) -> str:
        query = f'SELECT user.user_id, user.username FROM user \
        INNER JOIN friend_list ON user.user_id = friend_list.user_id WHERE friend_list.friend_id = {str(user_id)} \
        AND request_accepted = 0;'
        return query

    @logged_method
    def revoke_friend_request(self, user_id, friend_id) -> str:
        # FIXME
        raise NotImplementedError('revoke_friend_request has not been implemented yet')
        query = f'SELECT friend_list.user_id, '

        return query

    @logged_method
    def logout(self, username) -> str:
        query = f"UPDATE user SET signon_token = null WHERE username = '{username}';"
        return query

    @logged_method
    def get_most_games_won(self, number_of_games) -> str:
        query = "select user.username, user_statistics.* from user inner join user_statistics on user.user_id = \
        user_statistics.user_id order by games_won desc limit " + str(
            number_of_games) + ";"
        return query

    @logged_method
    def get_longest_win_streak(self, number_of_games) -> str:
        query = "select user.username, user_statistics.* from user \
        inner join user_statistics on user.user_id = user_statistics.user_id\
        order by longest_win_streak desc limit" + str(number_of_games) + ";"
        return query

    @logged_method
    def get_account_info(self, username) -> str:
        query = "SELECT user.avatar, user.chess_board_style,  user.chess_piece_style, \
        user.match_clock_choice, user.automatic_queueing, user.disable_pausing, user.require_commit_press, \
        user_statistics.level FROM user inner join user_statistics on user.user_id = user_statistics.user_id \
        Where username = '" + str(username) + "';"
        return query

    @logged_method
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

    @logged_method
    def save_account_info_by_key(self, username, key, value) -> Optional[str]:
        column = self.get_column(key)
        if (column is None):
            return None
        query = "UPDATE user, user_statistics SET " + str(column) + " = " + str(
            value) + " WHERE user.username = '" + str(username) + "';"
        return query

    @logged_method
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
