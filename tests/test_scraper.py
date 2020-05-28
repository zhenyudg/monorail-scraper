from unittest import TestCase

from scraper import MonorailScraper

test_url_1 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000'

class TestScraper(TestCase):

    scraper: MonorailScraper

    @classmethod
    def setUpClass(cls):
        cls.scraper = MonorailScraper()

    def test_get_issue(self):
        # this is a smoke test
        issue = self.scraper._get_issue(test_url_1)
        assert issue is not None and len(issue.text) > 0
