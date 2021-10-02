import mysql.connector
from database.MysqlDB import MysqlDB
from global_logger import logger, VERBOSE
import inspect
#from queryBuilder import queryBuilder

#MysqlDB is a class used to implement common database queries programaticly. It
#uses the querryBuilder class which holds the actual mysql syntax.
class DB:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, user, password, reader, writer, database):
        self.builder = MysqlDB()
        self.user = user
        self.password = password
        self.reader = reader
        self.writer = writer
        self.database = database

    def dbInsert(self, statement):
        logger.debug(f"func dbInsert -> statement: {statement}")
        try:
            mydb = mysql.connector.connect(user=self.user, password=self.password,
                                  host=self.writer,
                                  database=self.database,
                                  auth_plugin='mysql_native_password')
            cursor = mydb.cursor()
            cursor.execute(statement)
            mydb.commit()
            result = True
        except mysql.connector.Error as error:
            logger.error(error)
            logger.debug(f"error in sql statement: {statement}")
            result = False
        finally:
            if(mydb.is_connected()):
                cursor.close()
                mydb.close()
            logger.debug(f"result: {result}")
            return result

    def dbFetch(self, statement):
        logger.debug(f"func dbFetch -> statement: {statement}")
        try:
            result = ''
            mydb = mysql.connector.connect(user=self.user, password=self.password,
                                  host=self.reader,
                                  database=self.database,
                                  auth_plugin='mysql_native_password')
            cursor = mydb.cursor()
            cursor.execute(statement)
            result = cursor.fetchall()
        except Error as e:
            logger.error(error)
            result = None
        finally:
            if(mydb.is_connected()):
                cursor.close()
                mydb.close()
            logger.debug(f"result: {result}")
            return result

    def dbUpdate(self, statement):
        logger.debug(f"func dbUpdate -> statement: {statement}")
        try:
            mydb = mysql.connector.connect(user=self.user, password=self.password,
                                  host=self.writer,
                                  database=self.database,
                                  auth_plugin='mysql_native_password')
            cursor = mydb.cursor()
            cursor.execute(statement)
            mydb.commit()
            result = True
        except mysql.connector.Error as error:
            logger.error(error)
            result = False
        finally:
            if(mydb.is_connected()):
                cursor.close()
                mydb.close()
            logger.debug(f"result: {result}")
            return result

    def dbDelete(self, statement):
        logger.debug(f"func dbDelete -> statement: {statement}")
        try:
            mydb = mysql.connector.connect(user=self.user, password=self.password,
                                  host=self.writer,
                                  database=self.database,
                                  auth_plugin='mysql_native_password')
            cursor = mydb.cursor()
            cursor.execute(statement)
            mydb.commit()
            result = True
        except mysql.connector.Error as error:
            logger.error(error)
            result = False
        finally:
            if(mydb.is_connected()):
                cursor.close()
                mydb.close()
            logger.debug(f"result: {result}")
            return result


    def getPasswordFor(self, username):
        self.log_function_name()
        result = self.dbFetch(self.builder.getPasswordFor(username))
        return result

    def incrementSigninFailed(self):
        self.log_function_name()
        return False

    def changePassword(self, username, password):
        self.log_function_name()
        status = self.dbUpdate(self.builder.changePassword(username, password))
        return status

    #Returns 1\true if exits, false\0 if not
    def validateUserExists(self, username):
        self.log_function_name()
        statement = self.builder.validateUserExists(username)
        result = self.dbFetch(statement)
        result = result[0][0]
        return result

    #Returns 1\true if exits, false\0 if not
    def validateUsernameAvailable(self, username):
        self.log_function_name()
        statement = self.builder.validateUsernameAvailable(username)
        result = self.dbFetch(statement)
        intResult = result[0][0]
        return intResult

    #Returns 1\true if exits, false\0 if not
    def checkIfFriendRequestExists(self, username, friendsUsername):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        friendsId = self.dbFetch(self.builder.getUserId(friendsUsername))
        if(userId == False):
            return False
        if(friendsId == False):
            return False
        userId = userId[0][0]
        friendsId = friendsId[0][0]
        result = self.dbFetch(self.builder.checkIfFriendRequestExists(userId, friendsId))
        intResult = result[0][0]
        return intResult

    def createUser(self, parsedData):
        self.log_function_name()
        id = self.dbFetch(self.builder.getLastUserId())
        id = str(id[0][0] + 1)
        statement = self.builder.createUser(id,parsedData)
        self.dbInsert(statement)
        result = self.dbInsert(self.builder.createUserStats(id))
        return result

    def signin(self, username, token, tokenCreationTime):
        self.log_function_name()
        result = self.dbUpdate(self.builder.signin(username,token,tokenCreationTime))
        return result

    def getToken(self,username):
        self.log_function_name()
        result = self.dbFetch(self.builder.getToken(username))
        return result

    def getTokenCreationTime(self,username):
        self.log_function_name()
        result = self.dbFetch(self.builder.getTokenCreationTime(username))
        return result

    def getFriendsList(self, username):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        result = self.dbFetch(self.builder.getFriendsList(userId[0][0]))
        return result

    def getUserInfo(self, username):
        self.log_function_name()

        return False

    def getUserStats(self, username):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        userId = str(userId[0][0])
        result = self.dbFetch(self.builder.getUserStats(userId))
        return result

    def sendFriendRequest(self, username, friendsUsername):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        friendsId = self.dbFetch(self.builder.getUserId(friendsUsername))
        if(userId == False):
            return False
        if(friendsId == False):
            return False
        userId = userId[0][0]
        friendsId = friendsId[0][0]
        result = self.dbInsert(self.builder.sendFriendRequest(userId,friendsId))
        return result

    def acceptFriendRequest(self, username, friendsUsername, acceptedRequest):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        friendsId = self.dbFetch(self.builder.getUserId(friendsUsername))
        if(userId == False):
            return False
        if(friendsId == False):
            return False
        friendsId = friendsId[0][0]
        userId = userId[0][0]
        result = self.dbUpdate(self.builder.acceptFriendRequest(userId, friendsId, acceptedRequest))
        self.dbUpdate(self.builder.addFriend(userId, friendsId))
        return result

    def removeFriend(self, username, friendsUsername):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        friendsId = self.dbFetch(self.builder.getUserId(friendsUsername))
        if(userId == False):
            return False
        if(friendsId == False):
            return False
        friendsId = friendsId[0][0]
        userId = userId[0][0]
        result = self.dbDelete(self.builder.removeFriend(userId, friendsId))
        self.dbDelete(self.builder.removeFriend(friendsId, userId))
        return result

    def checkForFriendRequests(self, username):
        self.log_function_name()
        userId = self.dbFetch(self.builder.getUserId(username))
        if(userId == False):
            return False
        userId = userId[0][0]
        result = self.dbFetch(self.builder.checkForFriendRequests(userId))
        return result

    def logout(self, username):
        self.log_function_name()
        self.dbUpdate(self.builder.logout(username))

    def getMostChessGamesWon(self, numberOfGames):
        self.log_function_name()
        result = self.dbFetch(self.builder.getMostGamesWon(numberOfGames))
        return result

    def getLongestWinStreak(self, numberOfGames):
        self.log_function_name()
        result = self.dbFetch(self.builder.getLongestWinStreak(numberOfGames))
        return result

    def getAccountInfo(self, username):
        self.log_function_name()
        result = self.dbFetch(self.builder.getAccountInfo(username))
        return result

    def saveAccountInfo(self, username, data):
        self.log_function_name()
        self.dbUpdate(self.builder.saveAccountInfo(username, data))

    def saveAccountInfoByKey(self, username, key, value):
        self.log_function_name()
        querry = self.builder.saveAccountInfoByKey(username, key, value);
        if(querry is None):
            return
        else:
            self.dbUpdate(querry)
