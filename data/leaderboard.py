"""This module holds the Leaderboard class used to retrieve leaderboard statistics"""

from data.message_item import MessageItem
from global_logger import logged_method


class Leaderboard:
    """The class allows for retrieval of leaderboard statistics."""

    def __init__(self, database):
        self.db = database

    @logged_method
    def get_longest_win_streak(self, req_item: MessageItem,
                               number_of_games) -> None:  # TODO put type hint for number_of_games
        """Gets the longest consecutive string of wins not including games results that are omitted from leaderboards.

        Args:
            req_item: The message received by the server.
            number_of_games: # TODO describe this argument

        Returns:
            None
        """
        resp = self.db.get_longest_win_streak(number_of_games)
        req_item.set_longest_win_streak_response(number_of_games, resp)

    @logged_method
    def get_most_chess_games_won(self, req_item: MessageItem, number_of_games) -> None:
        """ TODO describe what this method does exactly...
                 If it just gets the number of games won, why have the word 'most'?

        Args:
            req_item: The message received by the server.
            number_of_games: TODO describe this argument

        Returns:
            None

        """
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

        req_item.set_most_chess_games_won_response(number_of_games, user_dict)
