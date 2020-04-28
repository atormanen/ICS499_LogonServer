import time
import json
#This class holds all the mysql syntax for the sql class
## TODO: change MysqlDB to db and change querry builder to mysqlQuerry
class MysqlDB:

    def __init__(self):
        self.tableName = 'test'

    def buildQuery(self, data):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        parsedData = json.loads(data)
        return insertStatement

    def getPasswordFor(self, username):
        selectStatement = "SELECT password FROM user WHERE username ='" +\
            username + "';"
        return selectStatement

    def changePassword(self, username, password):
        querry = "UPDATE user SET password = '" + str(password) + "' WHERE username = '" + str(username) +"';"
        print(querry)
        return querry

    def validateUserExists(self,username):
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" +\
            username + "');"
        return statement

    def checkIfFriendRequestExists(self, userId, friendsId):
        querry = "SELECT EXISTS(SELECT user_id FROM friend_list WHERE user_id = \
        " + str(userId) + " AND friend_id = " + str(friendsId) + " AND request_accepted = 0);"
        print(querry)
        return querry

    def validateUsernameAvailable(self,username):
        statement = "SELECT EXISTS(SELECT username FROM user WHERE username = '" +\
            username + "');"
        return statement

    def getLastUserId(self):
        return "SELECT MAX(user_id) FROM user;"

    def createUser(self, id, parsedData):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        return "INSERT INTO user VALUES("+ id +",'" + parsedData["username"] +\
            "','" +parsedData["firstName"] + "','" + parsedData["lastName"] + "',0," + \
            "'" + parsedData["email"] + "',0,'" + parsedData["password"] +\
            "','" + now + "','" + "null" +\
             "');"

    def createUserStats(self, id):
        return "INSERT INTO user_statistics VALUES("+ id +" ,0,0,0,0,0,1);"

    def getFriendsList(self, id):
        querry = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(id) + \
                    " AND request_accepted = 1;"
        return querry

    def getUserId(self, username):
        querry = "SELECT user_id FROM user WHERE username = '" + username + "';"
        return querry

    def getUserFromId(self, userId):
        querry = "SELECT username FROM user WHERE user_id = '" + str(userId) + "';"
        return querry

    def getUserStats(self, id):
        querry = "SELECT * FROM user_statistics WHERE user_id = " + id + ";"
        return querry

    def signin(self, username, token, tokenExpiration):
        querry = "UPDATE user SET token_creation='"+tokenExpiration + \
                    "',signon_token='" + token + "' WHERE username = " + \
                    "'" + username + "';"
        print(querry)
        return querry

    def getToken(self,username):
        querry = "SELECT signon_token FROM user WHERE username='" + username + "';"
        return querry

    def getTokenCreationTime(self,username):
        querry = "SELECT unix_timestamp(token_creation) FROM user WHERE username='" + username + "';"
        return querry

    def sendFriendRequest(self, user_id, friend_id):
        querry = "INSERT INTO friend_list VALUES(" + str(user_id) +\
                    ","+ str(friend_id) + ",0);"
        return querry

    def addFriend(self, userId, friendId):
        querry = "INSERT INTO friend_list VALUES(" + str(friendId) +\
                    ","+ str(userId) + ",1);"
        print(querry)
        return querry

    #UserId and friendId are backwards... that is intentional
    def acceptFriendRequest(self, userId, friendId, acceptedRequest):
        querry = "UPDATE friend_list set request_accepted = " + str(acceptedRequest) +\
                    " WHERE friend_id = " + str(userId) + " AND user_id = " +\
                    str(friendId) + ";"
        print(querry)
        return querry

    def removeFriend(self, userId, friendId):
        querry = "DELETE FROM friend_list WHERE user_id = " + str(userId) + " AND friend_id = " + str(friendId) + ";"
        print(querry)
        return querry

    def checkForFriendRequests(self, userId):
        querry = "select friend_list.user_id, user.username \
        from user \
        inner join friend_list \
        on user.user_id = friend_list.user_id\
        where friend_list.friend_id = " + str(userId) + \
        " AND request_accepted = 0;"
        print(querry)
        return querry

    def logout(self, username):
        querry = "UPDATE user SET signon_token = 'null' WHERE username = '" + \
                username + "';"
        print(querry)
        return querry

    def getMostGamesWon(self, numberOfGames):
        querry = "select user.username, user_statistics.* from user inner join user_statistics on user.user_id = user_statistics.user_id order by games_won desc limit " + str(numberOfGames) + ";"
        print(querry)
        return querry

    def getLongestWinStreak(self, numberOfGames):
        querry = "select user.username, user_statistics.* from user \
        inner join user_statistics on user.user_id = user_statistics.user_id\
        order by longetst_win_streak desc limit" + str(numberOfGames) + ";"
        print(querry)
        return querry
