from unittest import TestCase

from issue_scraper import IssueScraper

test_url_1 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000'


class TestIssueScraper(TestCase):

    scraper: IssueScraper

    @classmethod
    def setUpClass(cls):
        cls.scraper = IssueScraper()

    def test_get_issue_elem(self):
        # this is a smoke test
        issue_elem = self.scraper._get_issue_elem(test_url_1)
        assert issue_elem is not None and len(issue_elem.text) > 0
