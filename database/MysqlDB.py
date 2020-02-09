import mysql.connector
from database.queryBuilder import queryBuilder

class MysqlDB:
    builder = ''
    #user = "admin"
    #password = "ICS4992020"
    #host = "chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com"
    #host = 'localhost'
    #database = "userdb"

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
        print("Inside db")
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              use_pure=False)
        cursor = cnx.cursor()

        cursor.execute(validateUserExists(username))
        result = cnx.fetchall()
        #cursor.close()
        #cnx.close()
        print(result)
        return result

    def validateUsernameAvailable(self, username):
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              auth_plugin='mysql_native_password')
        cursor = cnx.cursor()

        cursor.execute(self.builder.validateUsernameAvailable(username))
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        intResult = result[0][0]
        return intResult

    def createUser(self, parsedData):

        cnx = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database,
                              auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
        cursor.execute(self.builder.getLastUserId())
        id = cursor.fetchall()
        id = str(id[0][0] + 1)
        cursor.execute(self.builder.createUser(id,parsedData))
        cnx.commit()
        cursor.execute(self.builder.createUserStats(id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return False

    def getFriendsList(self, username, userId):
        return False

    def getUserInfo(self, username, userId):
        return False

    def getUserStats(self, username, userId):
        return False
