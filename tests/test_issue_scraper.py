from unittest import TestCase

from issue_scraper import IssueScraper

test_url_1 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000'


class TestIssueScraper(TestCase):

    scraper: IssueScraper

    @classmethod
    def setUpClass(cls):
        cls.scraper = IssueScraper()

    def test_get_issue(self):
        # this is a smoke test
        issue = self.scraper._get_issue(test_url_1)
        assert issue is not None and len(issue.text) > 0
