import inspect
import time

from global_logger import logger, VERBOSE

# This class holds all the mysql syntax for the sql class
# TODO: change MysqlDB to db and change querry builder to mysqlQuerry
class MysqlDB:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self):
        self.tableName = 'test'


    def getPasswordFor(self, username):
        self.log_function_name()
        selectStatement = "SELECT password FROM user WHERE username ='" + \
                          username + "';"
        return selectStatement


    def changePassword(self, username, password):
        self.log_function_name()
        querry = "UPDATE user SET password = '" + str(password) + "' WHERE username = '" + str(username) + "';"
        return querry


    def validateUserExists(self, username):
        self.log_function_name()
        sql_statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return sql_statement


    def checkIfFriendRequestExists(self, userId, friendsId):
        self.log_function_name()
        sql_statement = "SELECT EXISTS(SELECT user_id FROM friend_list WHERE user_id = \
        " + str(userId) + " AND friend_id = " + str(friendsId) + " AND request_accepted = 0);"
        return sql_statement


    def validateUsernameAvailable(self, username):
        self.log_function_name()
        sql_statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return sql_statement


    def getLastUserId(self):
        self.log_function_name()
        return "SELECT MAX(user_id) FROM user;"


    def createUser(self, id, parsedData):
        self.log_function_name()
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        id = str(id)
        username = parsedData["username"]
        fname = parsedData["first_name"]
        lname = parsedData["last_name"]
        email = parsedData["email"]
        password = parsedData["password"]
        sql_staement = f"INSERT INTO user VALUES({id},'{username}','{fname}','{lname}','{email}',0,'{password}',null,'{now}',1,1,1,1,False,True,1);"
        return sql_staement


    def createUserStats(self, id):
        self.log_function_name()
        sql_statement = "INSERT INTO user_statistics VALUES(" + str(id) + ",0,0,0,0,0,null,1);"
        return sql_statement


    def getFriendsList(self, id):
        self.log_function_name()
        sql_statement = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(id) + \
                 " AND request_accepted = 1;"
        return sql_statement


    def getUserId(self, username):
        self.log_function_name()
        sql_statement = "SELECT user_id FROM user WHERE username = '" + username + "';"
        return sql_statement


    def getUserFromId(self, userId):
        self.log_function_name()
        sql_statement = "SELECT username FROM user WHERE user_id = '" + str(userId) + "';"
        return sql_statement


    def getUserStats(self, id):
        self.log_function_name()
        sql_statement = "SELECT * FROM user_statistics WHERE user_id = " + id + ";"
        return sql_statement


    def signin(self, username, token, tokenExpiration):
        self.log_function_name()
        sql_statement = "UPDATE user SET token_creation='" + tokenExpiration + \
                 "',signon_token='" + token + "' WHERE username = " + \
                 "'" + username + "';"
        return sql_statement


    def getToken(self, username):
        self.log_function_name()
        sql_statement = "SELECT signon_token FROM user WHERE username='" + username + "';"
        return sql_statement


    def getTokenCreationTime(self, username):
        self.log_function_name()
        sql_statement = "SELECT unix_timestamp(token_creation) FROM user WHERE username='" + username + "';"
        return sql_statement


    def sendFriendRequest(self, user_id, friend_id):
        self.log_function_name()
        sql_statement = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                 "," + str(friend_id) + ",0);"
        return sql_statement


    def addFriend(self, userId, friendId):
        self.log_function_name()
        sql_statement = "INSERT INTO friend_list VALUES(" + str(userId) + \
                 "," + str(friendId) + ",1);"
        return sql_statement


    # UserId and friendId are backwards... that is intentional
    def acceptFriendRequest(self, userId, friendId, acceptedRequest):
        self.log_function_name()
        sql_statement = "UPDATE friend_list set request_accepted = " + str(acceptedRequest) + \
                 " WHERE friend_id = " + str(userId) + " AND user_id = " + \
                 str(friendId) + ";"
        return sql_statement


    def removeFriend(self, userId, friendId):
        self.log_function_name()
        sql_statement = "DELETE FROM friend_list WHERE user_id = " + str(userId) + " AND friend_id = " + str(friendId) + ";"
        return sql_statement


    def checkForFriendRequests(self, user_id):
        self.log_function_name()
        sql_statement = f'SELECT user.user_id, user.username FROM user \
        INNER JOIN friend_list ON user.user_id = friend_list.user_id WHERE friend_list.friend_id = {str(user_id)} \
        AND request_accepted = 0;'
        return sql_statement


    def revokeFriendRequest(self, userId, friendId):
        self.log_function_name()
        # FIXME
        raise NotImplementedError('revokeFriendRequest has not been implemented yet')
        sql_statement = f'SELECT friend_list.user_id, '
        return sql_statement

    def logout(self, username):
        self.log_function_name()
        sql_statement = f"UPDATE user SET signon_token = null WHERE username = '{username}';"
        return sql_statement


    def getMostGamesWon(self, numberOfGames):
        self.log_function_name()
        sql_statement = "select user.username, user_statistics.* from user inner join user_statistics on user.user_id = user_statistics.user_id order by games_won desc limit " + str(
            numberOfGames) + ";"
        return sql_statement


    def getLongestWinStreak(self, numberOfGames):
        self.log_function_name()
        sql_statement = "select user.username, user_statistics.* from user \
        inner join user_statistics on user.user_id = user_statistics.user_id\
        order by longetst_win_streak desc limit" + str(numberOfGames) + ";"
        return sql_statement


    def getAccountInfo(self, username):
        self.log_function_name()
        sql_statement = "SELECT user.avatar, user.chess_board_style,  user.chess_piece_style, \
        user.match_clock_choice, user.automatic_queueing, user.disable_pausing, user.require_commit_press, user_statistics.level FROM user \
        inner join user_statistics on user.user_id = user_statistics.user_id \
        Where username = '" + str(username) + "';"
        return sql_statement


    def saveAccountInfo(self, username, data):
        self.log_function_name()
        sql_statement = "UPDATE user, user_statistics SET user.avatar = " + str(
            data["avatar_style"]) + ", user.chess_board_style = " + str(
            data["chess_board_style"]) + ", user.chess_piece_style = " + str(data["chess_piece_style"]) + \
                 ", user.match_clock_choice =  " + str(
            data["match_clock_choice"]) + ", user.automatic_queueing = " + str(
            data["automatic_queueing"]) + ", user.disable_pausing = " + str(data["disable_pausing"]) + \
                 ", user.require_commit_press =  " + str(
            data["require_commit_press"]) + ", user_statistics.level = " + str(
            data["level"]) + " WHERE user.username = '" + str(username) + "';"
        return sql_statement


    def saveAccountInfoByKey(self, username, key, value):
        self.log_function_name()
        column = self.getColumn(key)
        if (column is None):
            return None
        sql_statement = "UPDATE user, user_statistics SET " + str(column) + " = " + str(
            value) + " WHERE user.username = '" + str(username) + "';"
        return sql_statement


    def getColumn(self, key):
        self.log_function_name()
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
