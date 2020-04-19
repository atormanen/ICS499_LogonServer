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
            user["username"] = item[i][0]
            user["user_id"] = item[i][1]
            user["games_played"] = item[i][2]
            user["games_won"] = item[i][3]
            user["games_resigned"] = item[i][4]
            user["score"] = item[i][5]
            user["longest_win_streak"] = item[i][6]
            user["shortest_game"] = item[i][7]
            userStr = "user" + str(i)
            userDict[userStr] = user
            print(user)
            i = i + 1

        jsonObj = json.dumps(userDict)
        print(jsonObj)

        reqItem.mostChessGamesWonResponse(numberOfGames, resp)
