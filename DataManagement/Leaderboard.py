import json
from global_logger import logger, VERBOSE

class Leaderboard:

    log_function_name = lambda x: logger.debug(f"func {inspect.stack()[1][3]}")

    def __init__(self, database):
        self.db = database

    def getLongestWinStreak(self, reqItem, numberOfGames):
        self.log_function_name()
        resp = self.db.getLongestWinStreak(numberOfGames)
        reqItem.longestWinStreakResponse(numberOfGames, resp)


    def getMostChessGamesWon(self, reqItem, numberOfGames):
        self.log_function_name()
        resp = self.db.getMostChessGamesWon(numberOfGames)

        userDict = {
                    "user0":"users"
        }
        i = 0
        for item in resp:
            user = {
                    "username":"",
                    "user_id":"",
                    "games_played":"",
                    "games_won":"",
                    "games_resigned":"",
                    "score":"",
                    "longest_win_streak":"",
                    "shortest_game":""
            }
            user["username"] = item[0]
            user["user_id"] = item[1]
            user["games_played"] = item[2]
            user["games_won"] = item[3]
            user["games_resigned"] = item[4]
            user["score"] = item[5]
            user["longest_win_streak"] = item[6]
            user["shortest_game"] = item[7]
            userStr = "user" + str(i)
            userDict[userStr] = user
            i = i + 1

        reqItem.mostChessGamesWonResponse(numberOfGames, userDict)
