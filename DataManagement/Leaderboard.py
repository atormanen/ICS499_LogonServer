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

        for item in resp:
            i = 0
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
            user["username"] = resp[i][0]
            user["user_id"] = resp[i][1]
            user["games_played"] = resp[i][2]
            user["games_won"] = resp[i][3]
            user["games_resigned"] = resp[i][4]
            user["score"] = resp[i][5]
            user["longest_win_streak"] = resp[i][6]
            user["shortest_game"] = resp[i][7]
            userDict[str("user" + i)] = user
            i = i + 1

        jsonObj = json.dumps(userDict)
        print(jsonObj)

        reqItem.mostChessGamesWonResponse(numberOfGames, resp)
