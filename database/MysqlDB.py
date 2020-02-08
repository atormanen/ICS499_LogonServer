import mysql.connector
from database.queryBuilder import queryBuilder

class MysqlDB:
    builder = ''
    user = "admin"
    password = "ICS4992020"
    host = "chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com"
    #host = 'localhost'
    database = "userdb"

    def __init__(self, user, password, host, database):
        self.builder = queryBuilder()
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def mysqlDump(self, data):
        insertStatement = self.builder.buildQuery(data)
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              use_pure=False)
        cursor = cnx.cursor()

        cursor.execute(insertStatement)
        cnx.commit()
        cursor.close()
        cnx.close()

    def getPasswordFor(self, username, userId):
        selectStatement = self.builder.getPasswordFor(username)
        cnx = mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.database,use_pure=True)
        cursor = cnx.cursor()

        data = cursor.execute(selectStatement)
        print(data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return self.builder.getPasswordFor(username)

    def incrementSigninFailed(self):
        return False

    def validateUserExists(self, username, userId):
        return False

    def validateUsernameAvailable(self, username):
        return False

    def createUser(self, parsedData):
        return False

    def getFriendsList(self, username, userId):
        return False

    def getUserInfo(self, username, userId):
        return False

    def getUserStats(self, username, userId):
        return False
