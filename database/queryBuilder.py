import time
import json
class queryBuilder:

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

    def validateUserExists(self,username):
        return "SELECT EXISTS(SLECT username FROM user WHERE username = " +\
            username + " );"

    def validateUsernameAvailable(self,username):
        return "SELECT EXISTS(SELECT username FROM user WHERE username = '" +\
            username + "' );"

    def getLastUserId(self):
        return "SELECT MAX(user_id) FROM user;"

    def createUser(self, id, parsedData):
        return "INSERT INTO user VALUES("+ id +",'" + parsedData["username"] +\
            "','" +parsedData["firstName"] + "','" + parsedData["lastName"] +\
            "','" + parsedData["email"] + "',0,'" + parsedData["password"] +\
             "');"

    def createUserStats(self, id):
        return "INSERT INTO user_statistics VALUES("+ id +" ,0,0,0,0,0,1);"

    def getFriendsList(self, id):
        querry = "select user.user_id, user.username \
                    from user \
                    inner join  friend_list \
                    on user.user_id = friend_list.friend_id \
                    where friend_list.user_id = " + str(id) + ";"
        return querry

    def getUserId(self, username):
        querry = "SELECT user_id FROM user WHERE username = " + username + ";"
        return querry

    def getUserStats(self, id):
        querry = "SELECT * FROM user_statistics WHERE user_id = " + id + ";"
