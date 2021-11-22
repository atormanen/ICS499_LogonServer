import unittest

import global_logger
from global_logger import logged_method, logged_function, logged_class_method, depreciated
from util.testing import EnhancedTestCase


class TestGlobalLogger(EnhancedTestCase):
    def test_logged_class_method(self):

        class Button:
            # noinspection PyMethodParameters,PyMissingOrEmptyDocstring
            @logged_class_method
            def push(cls, times_pressed=1) -> str:
                tmp_str = f' {times_pressed} times' if times_pressed > 1 else ''
                return f'Someone pushed the button{tmp_str}'

        with self.subTest('kwargs'):

            global_logger._SINGLE_LINE_MODE = True

            expected_return_value_string = 'Someone pushed the button 3 times'

            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            actual_return_value_string = Button.push(times_pressed=3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0])

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'method': 'Button.push'",
                                           "'kwargs': {'times_pressed': 3}",
                                           "'args': ()",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')

        with self.subTest('positional_args'):
            expected_return_value_string = 'Someone pushed the button 3 times'

            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            # noinspection PyTypeChecker
            actual_return_value_string = Button.push(3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0])

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'method': 'Button.push'",
                                           "'args': (3,)",
                                           "'kwargs': {}",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')

    def test_logged_method(self):

        class Button:
            @logged_method
            def push(self, times_pressed=1) -> str:
                tmp_str = f' {times_pressed} times' if times_pressed > 1 else ''
                return f'Someone pushed the button{tmp_str}'

            def __repr__(self):
                return 'A simple button'

        with self.subTest('kwargs'):

            global_logger._SINGLE_LINE_MODE = True

            expected_return_value_string = 'Someone pushed the button 3 times'

            button = Button()
            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            actual_return_value_string = button.push(times_pressed=3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0])

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'method': 'Button.push'",
                                           "'kwargs': {'times_pressed': 3}",
                                           "'args': ()",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')

        with self.subTest('positional_args'):
            expected_return_value_string = 'Someone pushed the button 3 times'

            button = Button()
            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            actual_return_value_string = button.push(3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0])

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'method': 'Button.push'",
                                           "'args': (3,)",
                                           "'kwargs': {}",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')

    def test_logged_function(self):

        @logged_function
        def push(times_pressed=1) -> str:
            tmp_str = f' {times_pressed} times' if times_pressed > 1 else ''
            return f'Someone pushed the button{tmp_str}'

        with self.subTest('kwargs'):

            global_logger._SINGLE_LINE_MODE = True

            expected_return_value_string = 'Someone pushed the button 3 times'

            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            actual_return_value_string = push(times_pressed=3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0])

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'function': 'push'",
                                           "'kwargs': {'times_pressed': 3}",
                                           "'args': ()",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')

        with self.subTest('positional_args'):
            expected_return_value_string = 'Someone pushed the button 3 times'

            length = []
            # noinspection PyUnusedLocal
            actual_added_lines = []
            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))

            actual_return_value_string = push(3)
            self.assertEqual(expected_return_value_string, actual_return_value_string,
                             f'The returned string "{actual_return_value_string}" did not match \
                             "{expected_return_value_string}" when pushing button.')

            with open('./logs/logon_server.log', 'r') as f:
                lines = f.read().splitlines()
                length.append(len(lines))
                actual_added_lines = lines[length[0]:]

            # make sure only one line was added
            self.assertEqual(1, length[1] - length[0], "The number of lines added was not 1")

            # check that the line has the correct function
            list_that_must_be_in_actual = ["'function': 'push'",
                                           "'args': (3,)",
                                           "'kwargs': {}",
                                           "'return_value': 'Someone pushed the button 3 times'"]

            for str_to_find in list_that_must_be_in_actual:
                self.assertTrue(str_to_find in actual_added_lines[-1],
                                f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')


if __name__ == '__main__':
    unittest.main()


class TestDepreciated(EnhancedTestCase):
    def test_depreciated(self):

        @depreciated
        def push(times_pressed=1) -> str:
            tmp_str = f' {times_pressed} times' if times_pressed > 1 else ''
            return f'Someone pushed the button{tmp_str}'

        expected_return_value_string = 'Someone pushed the button 3 times'

        length = []
        # noinspection PyUnusedLocal
        actual_added_lines = []
        with open('./logs/logon_server.log', 'r') as f:
            lines = f.read().splitlines()
            length.append(len(lines))

        actual_return_value_string = push(3)

        with open('./logs/logon_server.log', 'r') as f:
            lines = f.read().splitlines()
            length.append(len(lines))
            actual_added_lines = lines[length[0]:]

        # make sure only one line was added
        self.assertEqual(1, length[1] - length[0], "The number of lines added was not 1")

        # check that the expected result was returned
        self.assertEqual(expected_return_value_string, actual_return_value_string,
                         f'The returned string "{actual_return_value_string}" did not match \
                         "{expected_return_value_string}" when pushing button.')

        # check that the expected content was logged
        list_that_must_be_in_actual = ['push is depreciated.']
        for str_to_find in list_that_must_be_in_actual:
            self.assertTrue(str_to_find in actual_added_lines[-1],
                            f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')


    def test_depreciated_with_alternitives(self):

        def push_a():
            ...

        def push_b():
            ...

        def push_c():
            ...

        class _TestData:
            def __init__(self, label, expected_str, alts):
                self.label = label
                self.expected_str = expected_str
                self.alts = alts

        data_list = [_TestData('push_a alt', 'push is depreciated, consider using push_a.', push_a),
                     _TestData('(push_a, push_b) alt', 'push is depreciated, consider using push_a or push_b.',
                               (push_a, push_b)),
                     _TestData('[push_a, push_b, push_c] alt', 'push is depreciated, consider using push_a, '
                                                               'push_b, or push_c.', [push_a, push_b, push_c])]
        for data in data_list:


            @self.inplace_subtest(data.label)
            def _():

                @depreciated(alternitives=data.alts)
                def push(times_pressed=1) -> str:
                    tmp_str = f' {times_pressed} times' if times_pressed > 1 else ''
                    return f'Someone pushed the button{tmp_str}'

                expected_return_value_string = 'Someone pushed the button 3 times'

                length = []
                # noinspection PyUnusedLocal
                actual_added_lines = []
                with open('./logs/logon_server.log', 'r') as f:
                    lines = f.read().splitlines()
                    length.append(len(lines))


                actual_return_value_string = push(3)

                # check that the correct value was returned
                self.assertEqual(expected_return_value_string, actual_return_value_string,
                                 f'The returned string "{actual_return_value_string}" did not match \
                                 "{expected_return_value_string}" when pushing button.')

                with open('./logs/logon_server.log', 'r') as f:
                    lines = f.read().splitlines()
                    length.append(len(lines))
                    actual_added_lines = lines[length[0]:]

                # make sure only one line was added
                self.assertEqual(1, length[1] - length[0])

                # check that the correct content was logged
                list_that_must_be_in_actual = [data.expected_str]
                for str_to_find in list_that_must_be_in_actual:
                    self.assertTrue(str_to_find in actual_added_lines[-1],
                                    f'"{str_to_find}" was not found in "{actual_added_lines[-1]}"')
