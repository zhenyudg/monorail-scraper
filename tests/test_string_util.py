from unittest import TestCase

from utils.string_util import *


class Test(TestCase):
    def test_almost_equal(self):
        self.assertTrue(almost_equal(None, None))
        self.assertFalse(almost_equal('', None))
        self.assertFalse(almost_equal(None, ''))

        self.assertTrue(almost_equal('abc', 'abc'))
        self.assertTrue(almost_equal('abc', 'ABC'))
        self.assertTrue(almost_equal('abc', 'abc '))
        self.assertTrue(almost_equal('abc', 'abc%'))

        self.assertTrue(almost_equal('ABC', 'abc'))
        self.assertTrue(almost_equal('abc ', 'abc'))
        self.assertTrue(almost_equal('abc%', 'abc'))
