class Leaderboard:
    def __init__(self, database):
        self.db = database

    def getLongestWinStreak(self, reqItem, numberOfGames):
        resp = self.db.getLongestWinStreak(numberOfGames)






        reqItem.longestWinStreakResponse(numberOfGames, resp)


    def getMostChessGamesWon(self, reqItem, numberOfGames):
        resp = self.db.getMostChessGamesWon(numberOfGames)

        print(type(resp))



        reqItem.mostChessGamesWonResponse(numberOfGames, resp)
