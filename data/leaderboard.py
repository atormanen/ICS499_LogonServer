"""This module holds the Leaderboard class used to retrieve leaderboard statistics"""
from data.message_item import GetLongestWinStreakRequest, GetMostChessGamesWonRequest
from database.db import FailureException


class Leaderboard:
    """The class allows for retrieval of leaderboard statistics."""

    def __init__(self, database):
        self.db = database

    # @logged_method
    def get_longest_win_streak(self, req_item: GetLongestWinStreakRequest,
                               number_of_games) -> None:  # TODO put type hint for number_of_games
        """Gets the longest consecutive string of wins not including games results that are omitted from leaderboards.

        Args:
            req_item: The message received by the server.
            number_of_games: # TODO describe this argument

        Returns:
            None
        """
        resp = self.db.get_longest_win_streak(number_of_games)
        req_item.set_response(number_of_games=number_of_games, data=resp)

    # @logged_method
    def get_most_chess_games_won(self, req_item: GetMostChessGamesWonRequest, number_of_games) -> None:
        """ TODO describe what this method does exactly...
                 If it just gets the number of games won, why have the word 'most'?

        Args:
            req_item: The message received by the server.
            number_of_games: TODO describe this argument

        Returns:
            None

        """
        try:
            resp = self.db.get_most_chess_games_won(number_of_games)

            user_dict = {
                'user0': 'users'
            }
            i = 0
            for item in resp:
                user = {'username': item[0], 'user_id': item[1], 'games_played': item[2], 'games_won': item[3],
                        'games_resigned': item[4], 'score': item[5], 'longest_win_streak': item[6],
                        'shortest_game': item[7]}
                user_str = 'user' + str(i)
                user_dict[user_str] = user
                i += 1
                req_item.set_response(number_of_games=number_of_games, data=user_dict)
        except FailureException as e:
            req_item.set_response(failure_reason=e.failure_reason_msg)
