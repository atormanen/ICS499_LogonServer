import time
import json
class queryBuilder:
    tableName = ''

    def __init__(self):
        self.tableName = 'test'

    def buildQuery(self, data):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        parsedData = json.loads(data)
        return insertStatement

    def getPasswordFor(self, username):
        selectStatement = "SELECT password from player where username ='" + username + "'"
        return selectStatement
