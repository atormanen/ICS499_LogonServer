import unittest
from unittest import TestCase

from data.message_item import *

if __name__ == '__main__':
    unittest.main()

EXPECTED_FAIL_STATUS = 'fail'
EXPECTED_SUCCESS_STATUS = 'success'

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


class Expected:
    ...


class TestBadRequest(TestCase):
    def test_response(self):
        expected = Expected()
        expected.request_type = 'some_invalid_request_type'
        expected.reason = "Invalid request_type 'some_invalid_request_type'. Please double check request syntax."
        expected.status = EXPECTED_FAIL_STATUS

        subtest_msgs = ['using builder', 'using constructor']

        def common_checks(req):
            self.assertIsInstance(req, BaseRequest)
            self.assertIsInstance(req, BadRequest)
            response = json.loads(req.response)
            self.assertEqual(expected.request_type, response['request_type'], f'{response!r}')
            self.assertEqual(expected.status, response['status'], f'{response!r}')
            self.assertEqual(expected.reason, response['reason'], f'{response!r}')

            for t in RequestType.values():
                self.assertIn(t, response['acceptable_request_types'], f'{response!r}')

        def get_generator(msg):
            return {'using builder': build_request,
                    'using constructor': BadRequest}[msg]

        for subtest_msg in subtest_msgs:
            with self.subTest(subtest_msg):
                socket = None
                parsed_data = {'request_type': expected.request_type}
                kwargs = {}
                generator = get_generator(subtest_msg)
                request = generator(socket, parsed_data, **kwargs)
                self.assertIsInstance(request, BadRequest, f'{request!r}')
                # request = generator(socket, parsed_data,  **kwargs)
                common_checks(request)

        del expected


class TestRevokeFriendRequestRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = REVOKE_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, RevokeFriendRequestRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = REVOKE_FRIEND_REQUEST
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=2, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, RevokeFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            del expected

        with self.subTest('fail response set'):
            socket = None
            expected = Expected()
            expected.request_type = REVOKE_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            expected.kwargs = dict(a=2, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, RevokeFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


# noinspection SpellCheckingInspection
class TestGetAccountInfoRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = GET_ACCOUNT_INFO
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, GetAccountInfoRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = GET_ACCOUNT_INFO
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.account_data = {'avatar_style': 1, 'chessboard_style': 2,
                                     'chesspiece_style': 3, 'match_clock_choice': 4,
                                     'automatic_queening': 5, 'disable_pausing': 6,
                                     'require_commit_press': 7, 'level': 8}
            expected.data = [list(expected.account_data.values())]

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetAccountInfoRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(account_data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.account_data.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = GET_ACCOUNT_INFO
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetAccountInfoRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response from no provided data'):
            expected = Expected()
            socket = None
            expected.request_type = GET_ACCOUNT_INFO
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - Account data was not found.'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetAccountInfoRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response()
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


class TestSaveAccountInfoByKeyRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = SAVE_ACCOUNT_INFO_BY_KEY
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, SaveAccountInfoByKeyRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )
            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = SAVE_ACCOUNT_INFO_BY_KEY
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = {'a': 1, 'b': 88}

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SaveAccountInfoByKeyRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = SAVE_ACCOUNT_INFO_BY_KEY
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = {'a': 1, 'b': 88}

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SaveAccountInfoByKeyRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestChangePasswordRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = CHANGE_PASSWORD
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, ChangePasswordRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = CHANGE_PASSWORD
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = {'a': 1, 'b': 2, 'c': 'hello'}

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, ChangePasswordRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = CHANGE_PASSWORD
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = {'a': 1, 'b': 2, 'c': 'hello'}

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, ChangePasswordRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestGetLongestWinStreakRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.number_of_games = 44
            expected.data = [2, 33]

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(number_of_games=expected.number_of_games, data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.number_of_games, response['number_of_games'], response)
            self.assertEqual(expected.data, response['data'], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('failure response from no number_of_games provided'):
            socket = None
            expected = Expected()
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_FAIL_STATUS
            expected.data = object()
            expected.failure_reason = 'Unexpected Error - User stats could not be found'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)
            self.assertNotIn('number_of_games', response)
            self.assertNotIn('data', response)

            del expected

        with self.subTest('failure response from no data provided'):
            socket = None
            expected = Expected()
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_FAIL_STATUS
            expected.number_of_games = object()
            expected.failure_reason = 'Unexpected Error - User stats could not be found'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(number_of_games=expected.number_of_games)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)
            self.assertNotIn('number_of_games', response)
            self.assertNotIn('data', response)

            del expected

        with self.subTest('failure response from nothing provided'):
            socket = None
            expected = Expected()
            expected.request_type = GET_LONGEST_WIN_STREAK
            expected.status = EXPECTED_FAIL_STATUS
            expected.number_of_games = object()
            expected.failure_reason = 'Unexpected Error - User stats could not be found'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetLongestWinStreakRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response()
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)
            self.assertNotIn('number_of_games', response)
            self.assertNotIn('data', response)

            del expected


class TestSignoutRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = SIGNOUT
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, SignoutRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = SIGNOUT
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=2, b='cat')

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SignoutRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = SIGNOUT
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = dict(a=2, b='cat')

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SignoutRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestRemoveFriendRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = REMOVE_FRIEND
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, RemoveFriendRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = REMOVE_FRIEND
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, RemoveFriendRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = REMOVE_FRIEND
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, RemoveFriendRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestAcceptFriendRequestRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = ACCEPT_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, AcceptFriendRequestRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = ACCEPT_FRIEND_REQUEST
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, AcceptFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = ACCEPT_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, AcceptFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestSendFriendRequestRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = SEND_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, SendFriendRequestRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = SEND_FRIEND_REQUEST
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SendFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = SEND_FRIEND_REQUEST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = dict(a=99, b=3)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SendFriendRequestRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


class TestGetFriendRequestsRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = GET_FRIEND_REQUESTS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, GetFriendRequestsRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = GET_FRIEND_REQUESTS
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.friends = ['Adam', 'Betty', 'Charlie']
            expected.count = 3
            friends_list_data = [[1, name, 'some other stuff'] for name in expected.friends]

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendRequestsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(friends_request_list=friends_list_data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.count, response['count'], f"counts don't match. {response!r}")

            actual_friends_usernames = [friend['username'] for friend in eval(response['friends'])]
            self.assertEqual(expected.count, len(actual_friends_usernames), f"count and len don't match. "
                                                                            f"{response['friends']!r}")

            for expected_username in expected.friends:
                self.assertIn(expected_username, actual_friends_usernames)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = GET_FRIEND_REQUESTS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendRequestsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response no friends list provided'):
            expected = Expected()
            socket = None
            expected.request_type = GET_FRIEND_REQUESTS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No friends list provided by server'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendRequestsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response()
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response bad friends list provided: list of strings'):
            expected = Expected()
            socket = None
            expected.request_type = GET_FRIEND_REQUESTS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - There was a problem reading friends list'

            bad_data = ['hello']

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendRequestsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(friends_request_list=bad_data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


class TestGetFriendsListRequest(TestCase):

    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = GET_FRIENDS_LIST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, GetFriendsListRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = GET_FRIENDS_LIST
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.friends = ['Adam', 'Betty', 'Charlie']
            expected.count = 3
            friends_list_data = [[1, name, 'some other stuff'] for name in expected.friends]

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendsListRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(friends_list=friends_list_data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.count, response['count'], f"counts don't match. {response!r}")

            actual_friends_usernames = [friend['username'] for friend in eval(response['friends'])]
            self.assertEqual(expected.count, len(actual_friends_usernames), f"count and len don't match. "
                                                                            f"{response['friends']!r}")

            for expected_username in expected.friends:
                self.assertIn(expected_username, actual_friends_usernames)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = GET_FRIENDS_LIST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendsListRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response no friends list provided'):
            expected = Expected()
            socket = None
            expected.request_type = GET_FRIENDS_LIST
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No friends list provided by server'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetFriendsListRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response()
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


class TestGetUserStatsRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = GET_USER_STATS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, GetUserStatsRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.request_type = GET_USER_STATS
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.user_stats = {'user_id': 1, 'games_played': 2,
                                   'games_won': 3, 'games_resigned': 4, 'score': 5,
                                   'longest_win_streak': 6}
            data = list(expected.user_stats.values())

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetUserStatsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(stats=data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.user_stats.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = GET_USER_STATS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetUserStatsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response no stats provided'):
            expected = Expected()
            socket = None
            expected.request_type = GET_USER_STATS
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - User stats could not be found'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetUserStatsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response()
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response invalid stats provided'):
            expected = Expected()
            socket = None
            expected.request_type = GET_USER_STATS
            expected.status = EXPECTED_FAIL_STATUS
            expected.user_stats = {'user_id': 1, 'games_played': 2,
                                   'games_won': 3, 'games_resigned': 4, 'score': 5}
            data = list(expected.user_stats.values())
            expected.failure_reason = 'Unexpected Error - User stats could not be found'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, GetUserStatsRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(stats=data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


class TestCreateAccountRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = CREATE_ACCOUNT
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, CreateAccountRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = CREATE_ACCOUNT
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.kwargs = dict(a=3, b=33)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, CreateAccountRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(**expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = CREATE_ACCOUNT
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'
            expected.kwargs = dict(a=3, b=33)

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, CreateAccountRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason, **expected.kwargs)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            for k, v in expected.kwargs.items():
                self.assertEqual(v, response[k], response)

            del expected


# noinspection SpellCheckingInspection,SpellCheckingInspection
class TestSigninRequest(TestCase):
    def test_response(self):
        with self.subTest('default fail response'):
            socket = None
            expected = Expected()
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No response set by server'
            parsed_data = dict(request_type=expected.request_type)
            request = build_request(socket, parsed_data)
            self.assertIsInstance(request, SigninRequest, f'{request!r}')
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'],
                             dict(msg='before setting response, it should be a fail',
                                  response=response))

            self.assertEqual(expected.failure_reason, response['reason'],
                             dict(msg='reason msg did not match',
                                  response=response)
                             )

            del expected

        with self.subTest('success response set'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_SUCCESS_STATUS
            expected.user_info = {'avatar_style': 1, 'chessboard_style': 2,
                                  'chesspiece_style': 3, 'match_clock_choice': 4,
                                  'automatic_queening': 5, 'disable_pausing': 6,
                                  'require_commit_press': 7, 'level': 8}
            expected.data = [list(expected.user_info.values())]

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SigninRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(token=expected.token, data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.token, response['token'], response)

            for k, v in expected.user_info.items():
                self.assertEqual(v, response[k], response)

            del expected

        with self.subTest('fail response set'):
            expected = Expected()
            socket = None
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'example failure reason'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SigninRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(failure_reason=expected.failure_reason)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response from no token provided'):
            socket = None
            expected = Expected()
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_FAIL_STATUS
            expected.user_info = {'avatar_style': 1, 'chessboard_style': 2,
                                  'chesspiece_style': 3, 'match_clock_choice': 4,
                                  'automatic_queening': 5, 'disable_pausing': 6,
                                  'require_commit_press': 7, 'level': 8}
            expected.data = [list(expected.user_info.values())]
            expected.failure_reason = 'Unexpected Error - No token provided by server.'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SigninRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response from no data provided'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_FAIL_STATUS
            expected.failure_reason = 'Unexpected Error - No user data received from database.'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SigninRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(token=expected.token)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected

        with self.subTest('fail response from invalid data provided'):
            socket = None
            expected = Expected()
            expected.token = 'example_token'
            expected.request_type = RequestType.SIGNIN
            expected.status = EXPECTED_FAIL_STATUS
            expected.user_info = {'avatar_style': 1, 'chessboard_style': 2}
            expected.data = [list(expected.user_info.values())]
            expected.failure_reason = 'Unexpected Error - Invalid user data received from database.'

            parsed_data = dict(request_type=expected.request_type)

            request = build_request(socket, parsed_data)

            self.assertIsInstance(request, BaseRequest, f'{request!r}')
            self.assertIsInstance(request, ValidRequest, f'{request!r}')
            self.assertIsInstance(request, SigninRequest, f'{request!r}')

            # noinspection PyUnresolvedReferences
            request.set_response(token=expected.token, data=expected.data)
            response = json.loads(request.response)

            self.assertEqual(expected.status, response['status'], response)
            self.assertEqual(expected.failure_reason, response['reason'], response)

            del expected


class TestFailureReasons(TestCase):
    def test_get_items(self):
        d = dict(U_BAD_FRIENDS_LIST_PROVIDED='Unexpected Error - There was a problem reading friends list',
                 U_ACCOUNT_DATA_NOT_FOUND='Unexpected Error - Account data was not provided by server.',
                 U_UNSPECIFIED='Unexpected Error - unspecified',
                 U_USER_STATS_COULD_NOT_BE_FOUND='Unexpected Error - User stats could not be found',
                 U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER='Unexpected Error - No friends list provided by server',
                 U_NO_RESPONSE_SET_BY_SERVER='Unexpected Error - No response set by server')

        self.assertEqual(6, len(FailureReasons.values()))

        for k, v in d.items():
            self.assertEqual(v, getattr(FailureReasons, k))

        for k, v in FailureReasons.items():
            self.assertEqual(d[k], v)


