import inspect
import time

from global_logger import logger, VERBOSE

# TODO: change MysqlDB to db and change querry builder to mysqlQuerry
class MysqlDB:
    """This class holds all the mysql syntax for the sql class"""
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
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

    def checkIfFriendRequestExists(self, userId, friendsId):
        self.log_function_name()
        querry = "SELECT EXISTS(SELECT user_id FROM friend_list WHERE user_id = \
        " + str(userId) + " AND friend_id = " + str(friendsId) + " AND request_accepted = 0);"
        return querry

    def validateUsernameAvailable(self, username):
        self.log_function_name()
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" + \
                    username + "');"
        return statement

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

    # id, username, firstname, lastname, email, avatar, ####, password, now, signonToken,

    def createUserStats(self, id):
        self.log_function_name()
        return "INSERT INTO user_statistics VALUES(" + str(id) + ",0,0,0,0,0,null,1);"

    def getFriendsList(self, id):
        self.log_function_name()
        querry = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(id) + \
                 " AND request_accepted = 1;"
        return querry

    def getUserId(self, username):
        self.log_function_name()
        querry = "SELECT user_id FROM user WHERE username = '" + username + "';"
        return querry

    def getUserFromId(self, userId):
        self.log_function_name()
        querry = "SELECT username FROM user WHERE user_id = '" + str(userId) + "';"
        return querry

    def getUserStats(self, id):
        self.log_function_name()
        querry = "SELECT * FROM user_statistics WHERE user_id = " + id + ";"
        return querry

    def signin(self, username, token, tokenExpiration):
        self.log_function_name()
        querry = "UPDATE user SET token_creation='" + tokenExpiration + \
                 "',signon_token='" + token + "' WHERE username = " + \
                 "'" + username + "';"
        return querry

    def getToken(self, username):
        self.log_function_name()
        querry = "SELECT signon_token FROM user WHERE username='" + username + "';"
        return querry

    def getTokenCreationTime(self, username):
        self.log_function_name()
        querry = "SELECT unix_timestamp(token_creation) FROM user WHERE username='" + username + "';"
        return querry

    def sendFriendRequest(self, user_id, friend_id):
        self.log_function_name()
        querry = "INSERT INTO friend_list VALUES(" + str(user_id) + \
                 "," + str(friend_id) + ",0);"
        return querry

    def addFriend(self, userId, friendId):
        self.log_function_name()
        querry = "INSERT INTO friend_list VALUES(" + str(userId) + \
                 "," + str(friendId) + ",1);"
        return querry

    # UserId and friendId are backwards... that is intentional
    def acceptFriendRequest(self, userId, friendId, acceptedRequest):
        self.log_function_name()
        querry = "UPDATE friend_list set request_accepted = " + str(acceptedRequest) + \
                 " WHERE friend_id = " + str(userId) + " AND user_id = " + \
                 str(friendId) + ";"
        return querry

    def removeFriend(self, userId, friendId):
        self.log_function_name()
        querry = "DELETE FROM friend_list WHERE user_id = " + str(userId) + " AND friend_id = " + str(friendId) + ";"
        return querry

    def checkForFriendRequests(self, userId):
        self.log_function_name()
        querry = "select friend_list.user_id, user.username \
        from user \
        inner join friend_list \
        on user.user_id = friend_list.user_id\
        where friend_list.friend_id = " + str(userId) + \
                 " AND request_accepted = 0;"
        return querry

    def logout(self, username):
        self.log_function_name()
        querry = f"UPDATE user SET signon_token = null WHERE username = '{username}';"
        return querry

    def getMostGamesWon(self, numberOfGames):
        self.log_function_name()
        querry = "select user.username, user_statistics.* from user inner join user_statistics on user.user_id = user_statistics.user_id order by games_won desc limit " + str(
            numberOfGames) + ";"
        return querry

    def getLongestWinStreak(self, numberOfGames):
        self.log_function_name()
        querry = "select user.username, user_statistics.* from user \
        inner join user_statistics on user.user_id = user_statistics.user_id\
        order by longetst_win_streak desc limit" + str(numberOfGames) + ";"
        return querry

    def getAccountInfo(self, username):
        self.log_function_name()
        querry = "SELECT user.avatar, user.chess_board_style,  user.chess_piece_style, \
        user.match_clock_choice, user.automatic_queueing, user.disable_pausing, user.require_commit_press, user_statistics.level FROM user \
        inner join user_statistics on user.user_id = user_statistics.user_id \
        Where username = '" + str(username) + "';"
        return querry

    def saveAccountInfo(self, username, data):
        self.log_function_name()
        querry = "UPDATE user, user_statistics SET user.avatar = " + str(
            data["avatar_style"]) + ", user.chess_board_style = " + str(
            data["chess_board_style"]) + ", user.chess_piece_style = " + str(data["chess_piece_style"]) + \
                 ", user.match_clock_choice =  " + str(
            data["match_clock_choice"]) + ", user.automatic_queueing = " + str(
            data["automatic_queueing"]) + ", user.disable_pausing = " + str(data["disable_pausing"]) + \
                 ", user.require_commit_press =  " + str(
            data["require_commit_press"]) + ", user_statistics.level = " + str(
            data["level"]) + " WHERE user.username = '" + str(username) + "';"
        return querry

    def saveAccountInfoByKey(self, username, key, value):
        self.log_function_name()
        column = self.getColumn(key)
        if (column is None):
            return None
        querry = "UPDATE user, user_statistics SET " + str(column) + " = " + str(
            value) + " WHERE user.username = '" + str(username) + "';"
        return querry

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
