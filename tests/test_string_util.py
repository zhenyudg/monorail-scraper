from unittest import TestCase

from monorail_scraper.utils.string_util import *


class Test(TestCase):
    def test_capture(self):
        self.assertEqual('world', capture('hello world', r'hello ([a-z]+)'))
        self.assertIsNone(capture('hello world', r'hello ([0-9]+)', fail_gently=True))

        with self.assertRaises(Warning):
            capture('hello world', r'hello ([0-9]+)')

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
