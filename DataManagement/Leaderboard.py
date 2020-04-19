import json

class Leaderboard:
    def __init__(self, database):
        self.db = database

    def getLongestWinStreak(self, reqItem, numberOfGames):
        resp = self.db.getLongestWinStreak(numberOfGames)






        reqItem.longestWinStreakResponse(numberOfGames, resp)


    def getMostChessGamesWon(self, reqItem, numberOfGames):
        resp = self.db.getMostChessGamesWon(numberOfGames)

        print(type(resp))
        userDict = {
                    "user0":"users"
        }
        print(resp)
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

        print(userDict)
        jsonObj = json.dumps(userDict)

        reqItem.mostChessGamesWonResponse(numberOfGames, jsonObj)
