"""This module holds the MessageItem class used to store incoming and outgoing messages"""
import json
from typing import Optional, Dict

from global_logger import logger, VERBOSE
import inspect


# Message item is a wrapper class to hold the data of each reqeust.
# It holds the json object that was sent to the server as well as
# the socket

# TODO: Create subclasses for each message type.
# Too much happening here


class RequestType:
    """Constants representing request types"""
    GET_ACCOUNT_INFO = 'getAccountInfo'
    SAVE_ACCOUNT_INFO_BY_KEY = 'saveAccountInfoByKey'
    CHANGE_PASSWORD = 'changePassword'
    GET_MOST_CHESS_GAMES_WON = 'get_most_chess_games_won'
    GET_LONGEST_WIN_STREAK = 'get_longest_win_streak'
    SIGNOUT = 'signout'
    REMOVE_FRIEND = 'removeFriend'
    ACCEPT_FRIEND_REQUEST = 'accept_friend_request'
    SEND_FRIEND_REQUEST = 'sendFriendRequest'
    GET_FRIEND_REQUESTS = 'getFriendRequests'
    GET_FRIENDS_LIST = 'getFriendsList'
    GET_USER_STATS = 'getUserStats'
    CREATE_ACCOUNT = 'createAccount'
    SIGNIN = 'signin'

    @classmethod
    def get_items(cls) -> list[str]:
        """Gets a list of all items"""
        return [RequestType.GET_ACCOUNT_INFO,
                RequestType.SAVE_ACCOUNT_INFO_BY_KEY,
                RequestType.CHANGE_PASSWORD,
                RequestType.GET_MOST_CHESS_GAMES_WON,
                RequestType.GET_LONGEST_WIN_STREAK,
                RequestType.SIGNOUT,
                RequestType.REMOVE_FRIEND,
                RequestType.ACCEPT_FRIEND_REQUEST,
                RequestType.SEND_FRIEND_REQUEST,
                RequestType.GET_FRIEND_REQUESTS,
                RequestType.GET_FRIENDS_LIST,
                RequestType.GET_USER_STATS,
                RequestType.CREATE_ACCOUNT,
                RequestType.SIGNIN]


class Status:
    """Constants representing possible Status values"""
    FAIL = 'fail'
    SUCCESS = 'success'

    @classmethod
    def get_items(cls) -> list[str]:
        """Gets a list of all items"""
        return [Status.FAIL, Status.SUCCESS]


class FailureReasons:
    """Constants representing failure reason messages"""
    UNSPECIFIED = 'unspecified'
    FRIENDS_LIST_WAS_NOT_FOUND = 'Friends list was not found.'
    USER_STATS_COULD_NOT_BE_FOUND = 'User stats could not be found'

    @classmethod
    def get_items(cls) -> list[str]:
        """Gets a list of all items"""
        return [FailureReasons.UNSPECIFIED,
                FailureReasons.FRIENDS_LIST_WAS_NOT_FOUND,
                FailureReasons.USER_STATS_COULD_NOT_BE_FOUND]


class MessageItem:
    """This class is used to store incoming and outgoing messages, storing and retreiving needed information."""
    log_function_name = lambda x: logger.debug(f'func {inspect.stack()[1][3]}')

    def __init__(self, connection_socket, parsed_data):
        self.connection_socket = connection_socket
        self.parsed_data = parsed_data
        self.response_obj = ''

    def set_invalid_request_response(self, request_type: Optional[str] = None,
                                     reason: Optional[str] = None, **kwargs) -> None:
        """Sets the response for an invalid request

        :param request_type: The type of request if it is recognized,
        else it is assumed to be an unrecognized request type.
        :param reason: The reason it is invalid, else the default reason will be
        'Invalid request. Please double check request syntax'
        :param kwargs: Any additional information to be sent.
        :return: None
        """
        self.log_function_name()
        self._set_failure_response(request_type=request_type if request_type else 'unknown_request_type',
                                   reason=reason if reason else 'Invalid request. Please double check request syntax',
                                   **kwargs)

    def set_signin_response(self, token: Optional[object], data: Optional[list],
                            failure_reason: Optional[str] = None) -> None:
        """Sets the response for a signin request

        :param token: TODO
        :param data: TODO
        :param failure_reason a string representation of the reason for the failure
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.SIGNIN
        user_dict = None
        if token and data and len(data) > 0 and len(data[0]) > 7:
            logger.debug(data)
            user_dict = {'token': token, 'avatar_style': data[0][0], 'chessboard_style': data[0][1],
                         'chesspiece_style': data[0][2], 'match_clock_choice': data[0][3],
                         'automatic_queening': data[0][4], 'disable_pausing': data[0][5],
                         'require_commit_press': data[0][6], 'level': data[0][7]}
        elif data:
            logger.debug(data)

        if user_dict:
            self._set_success_response(request_type, **user_dict)
        else:
            self._set_failure_response(request_type, failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def _set_success_response(self, request_type: str, **kwargs) -> None:
        """Sets the response for a successful operation

        :param request_type: The type of requests
        :param kwargs: Any other data needed by as part of the response.
        This will be appended in the json response message.
        :return: None
        """
        self.log_function_name()
        response = {
            'request_type': request_type,
            'status': Status.SUCCESS
        }

        for key, val in kwargs.items():
            # TODO Might want to add some value validation or processing
            response[key] = val

        self.response_obj = json.dumps(response)

    def _set_failure_response(self, request_type: str, reason: str, **kwargs) -> None:
        """Sets the response for a failed operation

        :param request_type: The type of requests
        :param reason: A message explaining why the request failed.
        :param kwargs: Any other data needed by as part of the response.
        This will be appended in the json response message.
        :return: None
        """
        self.log_function_name()
        response = {
            'request_type': request_type,
            'status': Status.FAIL,
            'reason': reason,
        }

        for key, val in kwargs.items():
            # TODO Might want to add some value validation or processing
            response[key] = val

        self.response_obj = json.dumps(response)

    def set_signin_response_failed(self, reason: str) -> None:
        """Sets the response for a failed signin request

        :param reason: the reason the signin attempt failed
        :return: None
        """
        self.log_function_name()
        self._set_failure_response(RequestType.SIGNIN, reason)

    def set_create_account_response(self, was_successful: bool, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to create an account.

        :param was_successful: True if account creation was successful, else False.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.CREATE_ACCOUNT
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type, failure_reason)

    def set_get_user_stats_response(self, stats: Optional[list], failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the user stats.

        :param stats: The user stats data to be sent.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.GET_USER_STATS
        if stats and len(stats) > 5:
            stat_dict = {'user_id': stats[0], 'games_played': stats[1],
                         'games_won': stats[2], 'games_resigned': stats[3], 'score': stats[4],
                         'longest_win_streak': stats[5]}
            self._set_success_response(request_type, **stat_dict)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else
                                       FailureReasons.USER_STATS_COULD_NOT_BE_FOUND)

    def set_get_friends_list_response(self, friends_list: Optional[list] = None,
                                      request_type: Optional[str] = None,
                                      failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get a friends list

        :param friends_list: The friends list data to send.
        :param request_type: The request type
        :param failure_reason: A message explaining the reason the operation failed.
        :return: None
        """
        self.log_function_name()

        if not request_type:
            request_type = RequestType.GET_FRIENDS_LIST

        if friends_list:
            friend_dict = {
                'friend0': 'friends'
            }

            i = 0
            for item in friends_list:
                user = {'username': item[1]}

                fried_str = 'friend' + str(i)
                friend_dict[fried_str] = user
                i = i + 1
            self._set_success_response(request_type, count=len(friends_list), friends=str(friend_dict))
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.FRIENDS_LIST_WAS_NOT_FOUND)

    def set_get_friend_requests_response(self, friends_list: Optional[list] = None,
                                         failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get friend requests

        :param friends_list: The friends list data.
        :param failure_reason: A message explaining why  the operation failed.
        :return: None
        """
        self.log_function_name()
        self.set_get_friends_list_response(friends_list=friends_list,
                                           request_type=RequestType.GET_FRIEND_REQUESTS,
                                           failure_reason=failure_reason)

    def set_accept_friend_request_response(self, was_successful: bool, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to accept a friend request

        :param was_successful: True if the operation was successful, else False.
        :param failure_reason: A message explaining why the operation failed
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.ACCEPT_FRIEND_REQUEST
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_send_friend_request_response(self, was_successful: bool,
                                         failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to send a friend request.

        :param was_successful: True if the opperation was successful, else false.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.SEND_FRIEND_REQUEST
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_remove_friend_response(self, was_successful: bool, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to remove a friend

        :param was_successful: True if the operation was successful, else False.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.REMOVE_FRIEND
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_signout_response(self, was_successful: bool, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to sign out

        :param was_successful: True if the operation was successful, else False.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.SIGNOUT
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_longest_win_streak_response(self, number_of_games: Optional[object], data: Optional[object],
                                        failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the longest win streak for a user.

        :param number_of_games: TODO
        :param data: TODO
        :param failure_reason: A message explaining why the operation failed
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.GET_LONGEST_WIN_STREAK
        if number_of_games and data:  # TODO Figure out if we should allow response with no data
            self._set_success_response(request_type, number_of_games=number_of_games, data=data)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_most_chess_games_won_response(self, number_of_games: Optional[object], data: Optional[object],
                                          failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the most games won

        :param number_of_games: TODO
        :param data: TODO
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.GET_MOST_CHESS_GAMES_WON
        if number_of_games and data:  # TODO Figure out if we should allow response with no data
            self._set_success_response(request_type, number_of_games=number_of_games, data=str(data))
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_change_password_response(self, was_successful: bool,
                                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to change a user's password

        :param was_successful: True if the operation was successful, else False.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.CHANGE_PASSWORD
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_save_account_info_by_key_response(self, was_successful: bool,
                                              failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to save account info by key

        :param was_successful: True if the operation was successful, else False.
        :param failure_reason: A message explaining why the operation failed.
        :return: None
        """
        self.log_function_name()
        request_type = RequestType.SAVE_ACCOUNT_INFO_BY_KEY
        if was_successful:
            self._set_success_response(request_type)
        else:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)

    def set_get_account_info_response(self, account_data: Optional[list],
                                      failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get account info

        :param account_data: The account data to be sent.
        :param failure_reason: A message explaining why the operation failed.
        :return:
        """
        self.log_function_name()
        request_type = RequestType.GET_ACCOUNT_INFO
        try:
            account_dict = {'avatar_style': account_data[0][0], 'chessboard_style': account_data[0][1],
                            'chesspiece_style': account_data[0][2], 'match_clock_choice': account_data[0][3],
                            'automatic_queening': account_data[0][4], 'disable_pausing': account_data[0][5],
                            'require_commit_press': account_data[0][6], 'level': account_data[0][7]}
            self._set_success_response(request_type, **account_dict)
        except IndexError or TypeError:
            self._set_failure_response(request_type,
                                       failure_reason if failure_reason else FailureReasons.UNSPECIFIED)
