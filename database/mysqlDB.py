import mysql.connector
from database.queryBuilder import queryBuilder

class mysqlDB:
    builder = queryBuilder('temperature')
    user = "admin"
    password = "ICS4992020"
    host = "chessgamedb.cxwhpucd0m6k.us-east-2.rds.amazonaws.com"
    database = ""

    def __init__(self, user, password, host, database):
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

    def getPassword(self,username):
        return false
