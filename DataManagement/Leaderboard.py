class Leaderboard:
    def __init__(self, database):
        self.db = database

    def getLongestWinStreak(self, reqItem, numberOfGames):
        resp = self.db.getLongestWinStreak(numberOfGames)






        reqItem.longestWinStreakResponse(numberOfGames, resp)


    def getMostChessGamesWon(self, reqItem, numberOfGames):
        resp = self.database.getMostChessGamesWon(numberOfGames)

        print(resp)



        reqItem.mostChessGamesWonResponse(numberOfGames, resp)
