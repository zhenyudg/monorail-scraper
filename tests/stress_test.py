import traceback
import unittest

from issue.issue_scraper import IssueScraper, get_issue_url
from oss_fuzz.oss_fuzz_bug_report_parser import attach_oss_fuzz_bug_report


class StressTest(unittest.TestCase):

    def test_stress(self):
        scraper = IssueScraper()
        url = get_issue_url('oss-fuzz', 24513)

        iterations = 200
        fails = 0

        for i in range(iterations):
            try:
                issue = scraper.scrape(url, loading_delay=0)
                attach_oss_fuzz_bug_report(issue)
            except Exception as e:
                print(f"Iteration {i} failed:")
                print(traceback.format_exc())
                fails += 1

        print(f"{fails} failed out of {iterations} iterations.")
