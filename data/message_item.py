"""This module holds the MessageItem class used to store incoming and outgoing messages"""
from __future__ import annotations
import json
from abc import abstractmethod, ABC
from typing import Optional, List, Protocol, runtime_checkable, Type, Dict, Tuple
from global_logger import logger, logged_method
from util.const import ConstContainerClass as ConstContainer

class RequestType(ConstContainer):
    """Constants representing request types."""

    REVOKE_FRIEND_REQUEST = 'revoke_friend_request'
    GET_ACCOUNT_INFO = 'get_account_info'
    SAVE_ACCOUNT_INFO_BY_KEY = 'save_account_info_by_key'
    CHANGE_PASSWORD = 'change_password'
    GET_MOST_CHESS_GAMES_WON = 'get_most_chess_games_won'
    GET_LONGEST_WIN_STREAK = 'get_longest_win_streak'
    SIGNOUT = 'signout'
    REMOVE_FRIEND = 'remove_friend'
    ACCEPT_FRIEND_REQUEST = 'accept_friend_request'
    SEND_FRIEND_REQUEST = 'send_friend_request'
    GET_FRIEND_REQUESTS = 'get_friend_requests'
    GET_FRIENDS_LIST = 'get_friends_list'
    GET_USER_STATS = 'get_user_stats'
    CREATE_ACCOUNT = 'create_account'
    SIGNIN = 'signin'


class Status(ConstContainer):
    """Constants representing possible Status values."""

    FAIL = 'fail'
    SUCCESS = 'success'

    @staticmethod
    def was_success(was_success: bool) -> str:
        """Gets the status given a boolean representing that the request was processed successfully.

        Args:
            was_success:
                A boolean representing that the request was processed successfully.

        Returns:
            Status.SUCCESS if was_success argument evaluates to True when converted to bool or
                Status.FAIL if was_success argument evaluates to False when converted to bool.

        """
        return Status.SUCCESS if bool(was_success) else Status.FAIL


class FailureReasons(ConstContainer):
    """Constants representing failure reason messages.
    A prefix of 'U_' indicates an unexpected error."""

    U_BAD_FRIENDS_LIST_PROVIDED = 'Unexpected Error - There was a problem reading friends list'
    U_ACCOUNT_DATA_NOT_FOUND = 'Unexpected Error - Account data was not provided by server.'
    U_UNSPECIFIED = 'Unexpected Error - unspecified'
    U_USER_STATS_COULD_NOT_BE_FOUND = 'Unexpected Error - User stats could not be found'
    U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER = 'Unexpected Error - No friends list provided by server'
    U_NO_RESPONSE_SET_BY_SERVER = 'Unexpected Error - No response set by server'


class BaseRequest(ABC):
    class Builder:
        @classmethod
        def build(cls, connection_socket, parsed_data: dict, *args, **kwargs) -> BaseRequest:
            selected_subclass = BadRequest
            request_type = parsed_data['request_type'] if \
                isinstance(parsed_data, dict) and 'request_type' in parsed_data.keys() else None
            if request_type:
                selected_subclass = cls._check_subclasses(ValidRequest, request_type)

            # noinspection PyTypeChecker
            return selected_subclass(connection_socket, parsed_data, *args, **kwargs)

        @classmethod
        def _check_subclasses(cls, class_to_check_subclasses: Type[BaseRequest], request_type):
            selected = None
            for subclass in class_to_check_subclasses.__subclasses__():
                try:
                    if subclass._get_request_type() == request_type:
                        return subclass
                except NotImplementedError:
                    continue
                selected = cls._check_subclasses(subclass, request_type)
            return selected if selected is not None else BadRequest

    def __init__(self, connection_socket, parsed_data: dict, *args, **kwargs):
        if not isinstance(parsed_data, dict):
            raise TypeError(f'parsed_data must be a dict, but it was {type(parsed_data).__name__}')
        self._connection_socket = connection_socket
        self._parsed_data: dict = parsed_data
        self._response: str = json.dumps({'request_type': self.request_type,
                                          'status': Status.FAIL,
                                          'reason': FailureReasons.U_NO_RESPONSE_SET_BY_SERVER})

    def __repr__(self):
        return f'{self.__dict__!r}'

    def __str__(self):
        return f'<{self.request_type!s} request>'

    @property
    def request_type(self) -> str:
        return self._parsed_data['request_type']

    @property
    def response(self):
        return self._response

    @property
    def parsed_data(self):
        return self._parsed_data

    @classmethod
    @abstractmethod
    def _get_request_type(cls) -> str:
        raise NotImplementedError


class ValidRequest(BaseRequest, ABC):

    @property
    def response(self):
        return self._response

    @response.deleter
    def response(self):
        self._response = ''

    def set_response(self, *, failure_reason: Optional[str] = None, **kwargs) -> None:
        """Sets the response.

        Args:
            failure_reason: If the operation fails,
                            this should be set to a non-empty string explaining why the operation failed.
            **kwargs: Any other information to be added in the response.

        Returns:
            None

        """
        was_successful = not failure_reason
        response = {'request_type': self.request_type,
                    'status': Status.was_success(was_successful)}
        if failure_reason:
            response['reason'] = failure_reason

        # Add extra key value pairs from keyword arguments
        for key, val in kwargs.items():
            if key not in response.keys():
                response[key] = val

        self._response = json.dumps(response)


class BadRequest(BaseRequest):

    def __init__(self, connection_socket, parsed_data: dict, *args, **kwargs):
        super().__init__(connection_socket, parsed_data, *args, **kwargs)

        self._response = json.dumps({'request_type': self.request_type,
                                     'status': Status.FAIL,
                                     'reason': f'Invalid request_type {self.request_type!r}. '
                                               f'Please double check request syntax.',
                                     'acceptable_request_types': RequestType.values()})

    @property
    def response(self):
        return self._response

    @classmethod
    def _get_request_type(cls) -> str:
        return 'unknown_request_type'


class RevokeFriendRequestRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.REVOKE_FRIEND_REQUEST


class GetAccountInfoRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_ACCOUNT_INFO

    @logged_method
    def set_response(self, *, account_data: Optional[list] = None, failure_reason: Optional[str] = None,
                     **kwargs) -> None:
        """Sets the response for a request to get account info.

        Args:
            account_data: The account data to be sent.
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """
        account_dict = {}
        if not failure_reason:
            try:
                # noinspection SpellCheckingInspection
                account_dict = {'avatar_style': account_data[0][0], 'chessboard_style': account_data[0][1],
                                'chesspiece_style': account_data[0][2], 'match_clock_choice': account_data[0][3],
                                'automatic_queening': account_data[0][4], 'disable_pausing': account_data[0][5],
                                'require_commit_press': account_data[0][6], 'level': account_data[0][7]}

            except IndexError or TypeError:
                failure_reason = FailureReasons.U_ACCOUNT_DATA_NOT_FOUND
        super().set_response(failure_reason=failure_reason, **account_dict)


class SaveAccountInfoByKeyRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.SAVE_ACCOUNT_INFO_BY_KEY

    @property
    def username(self):
        return self.parsed_data['username']

    @property
    def signon_token(self):
        return self.parsed_data['signon_token']

    @property
    def hash_val(self):
        return self.parsed_data['hash']

    @property
    def key(self):
        return self.parsed_data['key']

    @property
    def value(self):
        return self.parsed_data['value']

    @property
    def type_val(self):
        return self.parsed_data["type"]


class ChangePasswordRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.CHANGE_PASSWORD

    @property
    def username(self):
        return self.parsed_data['username']

    @property
    def old_password(self):
        return self.parsed_data['old_password']

    @property
    def new_password(self):
        return self.parsed_data['new_password']


class GetMostChessGamesWonRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_MOST_CHESS_GAMES_WON

    @logged_method
    def set_response(self,
                     number_of_games: Optional[object] = None,
                     data: Optional[dict] = None,
                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the most games won

        Args:
            number_of_games: TODO
            data: TODO
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """
        data_dict = {}
        if not failure_reason:
            if number_of_games and data:
                data_dict = dict(number_of_games=number_of_games, data=str(data))
            else:
                failure_reason = FailureReasons.U_USER_STATS_COULD_NOT_BE_FOUND
        super().set_response(failure_reason=failure_reason, **data_dict)


class GetLongestWinStreakRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_LONGEST_WIN_STREAK

    @logged_method
    def set_response(self, *, number_of_games: Optional[object] = None, data: Optional[object] = None,
                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the longest win streak for a user.

        Args:
            number_of_games: TODO
            data: TODO
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        data_dict = {}
        if not failure_reason:
            if number_of_games is not None and data is not None:
                data_dict = dict(number_of_games=number_of_games, data=data)
            else:
                failure_reason = FailureReasons.U_USER_STATS_COULD_NOT_BE_FOUND

        super().set_response(failure_reason=failure_reason, **data_dict)


class SignoutRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.SIGNOUT


class RemoveFriendRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.REMOVE_FRIEND


class AcceptFriendRequestRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.ACCEPT_FRIEND_REQUEST


class SendFriendRequestRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.SEND_FRIEND_REQUEST


class GetFriendRequestsRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_FRIEND_REQUESTS

    @logged_method
    def set_response(self, *,
                     friends_list: Optional[list] = None,
                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get friend requests

        Args:
            friends_list: The friends list data. This is a list of TODO What is the element of the list?
                                                                        a tuple, dict, list?
            failure_reason: A message explaining why  the operation failed.

        Returns:
            None

        """

        friends_list_dict = {}
        if not failure_reason:
            if isinstance(friends_list, list):
                try:
                    if len(friends_list) > 0 and not isinstance(friends_list[0], list):
                        raise TypeError
                    new_friends_list = [{'username': item[1]} for item in friends_list]
                    friends_list_dict = dict(count=len(new_friends_list), friends=str(new_friends_list))
                except (IndexError, TypeError) as e:
                    failure_reason = FailureReasons.U_BAD_FRIENDS_LIST_PROVIDED
            else:
                failure_reason = FailureReasons.U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER

        super().set_response(failure_reason=failure_reason, **friends_list_dict)


class GetFriendsListRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_FRIENDS_LIST

    @logged_method
    def set_response(self, *,
                     friends_list: Optional[list] = None,
                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get a friends list

        Args:
            friends_list: The friends list data to send. This is a list of TODO What is the element of the list?
                                                                                a tuple, dict, list?
            failure_reason: A message explaining the reason the operation failed.

        Returns:
            None

        """
        friends_list_dict = {}
        if not failure_reason:
            if isinstance(friends_list, list):
                try:
                    if len(friends_list) > 0 and not isinstance(friends_list[0], list):
                        raise TypeError
                    new_friends_list = [{'username': item[1]} for item in friends_list]
                    friends_list_dict = dict(count=len(new_friends_list), friends=str(new_friends_list))
                except (IndexError, TypeError) as e:
                    failure_reason = FailureReasons.U_BAD_FRIENDS_LIST_PROVIDED
            else:
                failure_reason = FailureReasons.U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER

        super().set_response(failure_reason=failure_reason, **friends_list_dict)


class GetUserStatsRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.GET_USER_STATS

    @property
    def username(self):
        return self.parsed_data['username']

    @logged_method
    def set_response(self, *, stats: Optional[list] = None, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the user stats.

        Args:
            stats:
                The user stats data to be sent.
            failure_reason:
                A message explaining why the operation failed.

        Returns:
            None

        """
        stat_dict = {}
        if not failure_reason:
            if stats and len(stats) > 5:
                stat_dict = {'user_id': stats[0], 'games_played': stats[1],
                             'games_won': stats[2], 'games_resigned': stats[3], 'score': stats[4],
                             'longest_win_streak': stats[5]}
            else:
                failure_reason = FailureReasons.U_USER_STATS_COULD_NOT_BE_FOUND

        super().set_response(failure_reason=failure_reason, **stat_dict)


class CreateAccountRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.CREATE_ACCOUNT


class SigninRequest(ValidRequest):
    @classmethod
    def _get_request_type(cls) -> str:
        return RequestType.SIGNIN

    # @logged_method
    def set_response(self, *,
                     token: Optional[object] = None,
                     data: Optional[list] = None,
                     failure_reason: Optional[str] = None) -> None:
        """Sets the response for a signin request.

        Args:
            token: TODO describe the token.
            data: TODO What is expected? What is the structure required?
            failure_reason: A string representation of the reason for the failure.

        Returns:
            None

        """

        request_type = RequestType.SIGNIN
        user_dict = {}
        if not failure_reason:
            if token:
                if data and len(data) > 0 and len(data[0]) > 7:
                    logger.debug(data)

                    # noinspection SpellCheckingInspection
                    user_dict = {'token': token, 'avatar_style': data[0][0], 'chessboard_style': data[0][1],
                                 'chesspiece_style': data[0][2], 'match_clock_choice': data[0][3],
                                 'automatic_queening': data[0][4], 'disable_pausing': data[0][5],
                                 'require_commit_press': data[0][6], 'level': data[0][7]}
                elif data:
                    logger.debug(data)
                    failure_reason = 'Unexpected Error - Invalid user data received from database.'
                else:
                    failure_reason = 'Unexpected Error - No user data received from database.'
            else:
                failure_reason = 'Unexpected Error - No token provided by server.'

        super().set_response(failure_reason=failure_reason, **user_dict)


def build_request(connection_socket, parsed_data: dict, *args, **kwargs) -> BaseRequest:
    return BaseRequest.Builder.build(connection_socket, parsed_data, *args, **kwargs)


class MessageItem:
    """This class is used to store incoming and outgoing messages, storing and retrieving needed information."""

    def __init__(self, connection_socket, parsed_data):
        self.connection_socket = connection_socket
        self.parsed_data = parsed_data
        self.response_obj = ''

    # def _set_response(self, request_type: str, failure_reason: Optional[str] = None, **kwargs) -> None:
    #     was_successful = not failure_reason
    #     response = {'request_type': request_type,
    #                 'status': Status.was_success(was_successful)}
    #     if failure_reason:
    #         response['reason'] = failure_reason
    #
    #     # Add extra key value pairs from keyword arguments
    #     for key, val in kwargs.values():
    #         if key not in response.keys():
    #             response[key] = val
    #
    #     self.response_obj = json.dumps(response)

    @logged_method
    def set_invalid_request_response(self, request_type: Optional[str] = None,
                                     failure_reason: Optional[str] = None, **kwargs) -> None:
        """Sets the response for an invalid request.

        Args:
            request_type:
                The type of request if it is recognized, else it is assumed to be an unrecognized request type.
            failure_reason:
                The reason it is invalid, else the default reason will be
                'Invalid request. Please double check request syntax'.
            **kwargs:
                Any additional information to be sent.

        Returns:
            None

        """

        self._set_response(request_type=request_type if request_type else 'unknown_request_type',
                           reason=failure_reason if failure_reason else 'Invalid request. Please double check request '
                                                                        'syntax.',
                           acceptable_request_types=RequestType.values(),
                           **kwargs)

    @logged_method
    def set_signin_response(self, token: Optional[object] = None, data: Optional[list] = None,
                            failure_reason: Optional[str] = None) -> None:
        """Sets the response for a signin request.

        Args:
            token: TODO describe the token.
            data: TODO What is expected? What is the structure required?
            failure_reason: A string representation of the reason for the failure.

        Returns:
            None

        """

        request_type = RequestType.SIGNIN
        user_dict = {}
        if not failure_reason:
            if token:
                if data and len(data) > 0 and len(data[0]) > 7:
                    logger.debug(data)

                    # noinspection SpellCheckingInspection
                    user_dict = {'token': token, 'avatar_style': data[0][0], 'chessboard_style': data[0][1],
                                 'chesspiece_style': data[0][2], 'match_clock_choice': data[0][3],
                                 'automatic_queening': data[0][4], 'disable_pausing': data[0][5],
                                 'require_commit_press': data[0][6], 'level': data[0][7]}
                elif data:
                    logger.debug(data)
                    failure_reason = 'Unexpected Error - Invalid user data received from database.'
                else:
                    failure_reason = 'Unexpected Error - No user data received from database.'
            else:
                failure_reason = 'Unexpected Error - No token provided by server.'

        self._set_response(request_type, failure_reason, **user_dict)

    @logged_method
    def set_signin_response_failed(self, failure_reason: str) -> None:
        """Sets the response for a failed signin request.

        Args:
            failure_reason:
                The reason the signin attempt failed.

        Returns:
            None

        """

        if not failure_reason:
            failure_reason = 'Unexpected Error - Signin failed, but no reason provided.'

        self._set_response(RequestType.SIGNIN, failure_reason)

    @logged_method
    def set_create_account_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to create an account.

        Args:
            failure_reason:
                A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.CREATE_ACCOUNT
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_get_user_stats_response(self, stats: Optional[list] = None, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the user stats.

        Args:
            stats:
                The user stats data to be sent.
            failure_reason:
                A message explaining why the operation failed.

        Returns:
            None

        """
        stat_dict = {}
        request_type = RequestType.GET_USER_STATS
        if not failure_reason:
            if stats and len(stats) > 5:
                stat_dict = {'user_id': stats[0], 'games_played': stats[1],
                             'games_won': stats[2], 'games_resigned': stats[3], 'score': stats[4],
                             'longest_win_streak': stats[5]}
            else:
                failure_reason = FailureReasons.USER_STATS_COULD_NOT_BE_FOUND

        self._set_response(request_type, failure_reason, **stat_dict)

    @logged_method
    def set_get_friends_list_response(self, friends_list: Optional[list] = None,
                                      request_type: Optional[str] = None,
                                      failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get a friends list

        Args:
            friends_list: The friends list data to send. This is a list of TODO What is the element of the list?
                                                                                a tuple, dict, list?
            request_type: The request type.
            failure_reason: A message explaining the reason the operation failed.

        Returns:
            None

        """
        friends_list_dict = {}
        if not request_type:
            request_type = RequestType.GET_FRIENDS_LIST

        if not failure_reason:
            new_friends_list = []
            if friends_list:
                for item in friends_list:
                    user = {'username': item[1]}

                    # fried_str = "friend" + str(i)
                    # friend_dict[friedStr] = user
                    new_friends_list.append(user)
            friends_list_dict = dict(count=len(new_friends_list), friends=str(new_friends_list))
        self._set_response(request_type, failure_reason, **friends_list_dict)

    @logged_method
    def set_get_friend_requests_response(self, friends_list: Optional[list] = None,
                                         failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get friend requests

        Args:
            friends_list: The friends list data. This is a list of TODO What is the element of the list?
                                                                        a tuple, dict, list?
            failure_reason: A message explaining why  the operation failed.

        Returns:
            None

        """

        self.set_get_friends_list_response(friends_list=friends_list,
                                           request_type=RequestType.GET_FRIEND_REQUESTS,
                                           failure_reason=failure_reason)

    @logged_method
    def set_accept_friend_request_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to accept a friend request.

        Args:
            failure_reason: A message explaining why the operation failed

        Returns:
            None

        """

        request_type = RequestType.ACCEPT_FRIEND_REQUEST
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_send_friend_request_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to send a friend request.

        Args:
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.SEND_FRIEND_REQUEST
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_remove_friend_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to remove a friend.

        Args:
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.REMOVE_FRIEND
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_signout_response(self, failure_reason: Optional[str] = None) -> None:
        """

        Args:
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.SIGNOUT
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_longest_win_streak_response(self, number_of_games: Optional[object] = None, data: Optional[object] = None,
                                        failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the longest win streak for a user.

        Args:
            number_of_games: TODO
            data: TODO
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.GET_LONGEST_WIN_STREAK
        data_dict = {}
        if not failure_reason:
            if number_of_games and data:
                data_dict = dict(number_of_games=number_of_games, data=data)
            else:
                failure_reason = FailureReasons.UNSPECIFIED

        self._set_response(request_type, failure_reason, **data_dict)

    @logged_method
    def set_most_chess_games_won_response(self, number_of_games: Optional[object] = None, data: Optional[object] = None,
                                          failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get the most games won

        Args:
            number_of_games: TODO
            data: TODO
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.GET_MOST_CHESS_GAMES_WON
        data_dict = {}
        if not failure_reason:
            if number_of_games and data:
                data_dict = dict(number_of_games=number_of_games, data=str(data))
            else:
                failure_reason = FailureReasons.UNSPECIFIED
        self._set_response(request_type, failure_reason, **data_dict)

    @logged_method
    def set_change_password_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to change a user's password.

        Args:
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.CHANGE_PASSWORD
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_save_account_info_by_key_response(self, failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to save account info by key.

        Args:
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.SAVE_ACCOUNT_INFO_BY_KEY
        self._set_response(request_type, failure_reason)

    @logged_method
    def set_get_account_info_response(self, account_data: Optional[list] = None,
                                      failure_reason: Optional[str] = None) -> None:
        """Sets the response for a request to get account info.

        Args:
            account_data: The account data to be sent.
            failure_reason: A message explaining why the operation failed.

        Returns:
            None

        """

        request_type = RequestType.GET_ACCOUNT_INFO
        account_dict = {}
        if not failure_reason:
            try:
                # noinspection SpellCheckingInspection
                account_dict = {'avatar_style': account_data[0][0], 'chessboard_style': account_data[0][1],
                                'chesspiece_style': account_data[0][2], 'match_clock_choice': account_data[0][3],
                                'automatic_queening': account_data[0][4], 'disable_pausing': account_data[0][5],
                                'require_commit_press': account_data[0][6], 'level': account_data[0][7]}

            except IndexError or TypeError:
                failure_reason = FailureReasons.UNSPECIFIED
        self._set_response(request_type, failure_reason, **account_dict)
