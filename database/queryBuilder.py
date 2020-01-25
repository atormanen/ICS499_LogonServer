import time
import json
class queryBuilder:
    tableName = ''

    def __init__(self, table):
        self.tableName = table

    def buildQuery(self, data):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        parsedData = json.loads(data)
        return insertStatement
