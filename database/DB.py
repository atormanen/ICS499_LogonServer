import mysql.connector
from database.MysqlDB import MysqlDB
#from queryBuilder import queryBuilder

#MysqlDB is a class used to implement common database queries programaticly. It
#uses the querryBuilder class which holds the actual mysql syntax.
class DB:

    def __init__(self, user, password, host, database):
        self.builder = MysqlDB()
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def dbInsert(self, statement):
        mydb = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              auth_plugin='mysql_native_password')
        cursor = mydb.cursor()
        cursor.execute(statement)
        mydb.commit()
        cursor.close()
        mydb.close()

    def dbFetch(self, statement):
        mydb = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              auth_plugin='mysql_native_password')
        cursor = mydb.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()
        return result

    def getPasswordFor(self, username):
        print('getting pass')
        result = self.dbFetch(self.builder.getPasswordFor(username))
        return result

    def incrementSigninFailed(self):
        return False

    def validatekUserExists(self, username):
        statement = self.builder.validateUserExists(username)
        result = self.dbFetch(statement)
        return result

    #Returns 1\true if exits, false\0 if not
    def validateUsernameAvailable(self, username):
        statement = self.builder.validateUsernameAvailable(username)
        result = self.dbFetch(statement)
        intResult = result[0][0]
        return intResult

    def createUser(self, parsedData):
        id = self.dbFetch(self.builder.getLastUserId())
        id = str(id[0][0] + 1)
        self.dbInsert(self.builder.createUser(id,parsedData))
        self.dbInsert(self.builder.createUserStats(id))


    def getFriendsList(self, username):
        result = self.dbFetch(self.builder.getFriendsList(userId))
        return result

    def getUserInfo(self, username):

        return False

    def getUserStats(self, username):
        id = self.dbFetch(builder.getUserId(username))
        result = self.dbFetch(self.builder.getUserStats(userId))
        return result
