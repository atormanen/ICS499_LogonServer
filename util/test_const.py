#!/usr/bin/env python3
from collections import Callable
from typing import Type
from unittest import TestCase
import unittest

from util.const import ConstContainerClass

if __name__ == '__main__':
    unittest.main()


# noinspection PyPep8Naming
class _TestTemplate:

    def __init__(self, test_case: unittest.TestCase, dictionary_of_expected_constants: dict,
                 class_to_test: Type[ConstContainerClass]):
        self._test_case = test_case
        self.expected_dict = dictionary_of_expected_constants
        self.const_cls = class_to_test

    def test_class_is_subclass_ConstContainerClass(self):
        self._test_case.assertTrue(issubclass(self.const_cls, ConstContainerClass))

    def test_values_match(self):
        self._test_case.assertEqual(len(self.expected_dict), len(self.const_cls.values()))

        for v in self.expected_dict.values():
            self._test_case.assertIn(v, self.const_cls.values())

    def test_items_match(self):
        self._test_case.assertEqual(len(self.expected_dict), len(self.const_cls.items()))

        for k, v in self.expected_dict.items():
            self._test_case.assertEqual(v, getattr(self.const_cls, k))

    def test_keys_match(self):
        self._test_case.assertEqual(len(self.expected_dict), len(self.const_cls.keys()))

        for k in self.expected_dict.keys():
            self._test_case.assertIn(k, self.const_cls.keys())

    def __call__(self) -> None:
        """Runs all tests in template"""
        # methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func))]
        test_methods = [(name, getattr(self, name)) for name in dir(self) if
                        isinstance(getattr(self, name), Callable) and name.startswith('test')]
        # self._test_case.assertEqual('', repr(methods))
        for name, test in test_methods:
            label = name
            if name not in ['test', 'test_']:
                label = name[4:].lstrip('_')
            with self._test_case.subTest(label):
                test()

            # if isinstance(test, Callable) and name.startswith('test'):
            #     # with self.test_case.subTest(name):
            #     #     test(self)


class TestConstContainerClass(TestCase):

    def test_string_contents_only(self):
            d = dict(U_BAD_FRIENDS_LIST_PROVIDED='Unexpected Error - There was a problem reading friends list',
                     U_ACCOUNT_DATA_NOT_FOUND='Unexpected Error - Account data was not provided by server.',
                     U_UNSPECIFIED='Unexpected Error - unspecified',
                     U_USER_STATS_COULD_NOT_BE_FOUND='Unexpected Error - User stats could not be found',
                     U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER='Unexpected Error - No friends list provided by server',
                     U_NO_RESPONSE_SET_BY_SERVER='Unexpected Error - No response set by server')

            class ConstantClass(ConstContainerClass):
                U_BAD_FRIENDS_LIST_PROVIDED = 'Unexpected Error - There was a problem reading friends list'
                U_ACCOUNT_DATA_NOT_FOUND = 'Unexpected Error - Account data was not provided by server.'
                U_UNSPECIFIED = 'Unexpected Error - unspecified'
                U_USER_STATS_COULD_NOT_BE_FOUND = 'Unexpected Error - User stats could not be found'
                U_NO_FRIENDS_LIST_PROVIDED_BY_SERVER = 'Unexpected Error - No friends list provided by server'
                U_NO_RESPONSE_SET_BY_SERVER = 'Unexpected Error - No response set by server'

            t = _TestTemplate(self, d, ConstantClass)
            t()

