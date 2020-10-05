from unittest import TestCase

from monorail_scraper.issue.issue_scraper import *

test_url_1 = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000'


class TestIssueScraper(TestCase):

    scraper: IssueScraper

    @classmethod
    def setUpClass(cls):
        cls.scraper = IssueScraper()

    def test_scrape(self):
        # smoke test
        issue = self.scraper.scrape(test_url_1)
        self.assertIsNotNone(issue)
        print(issue)

    def test_scrape_nonexisting_issue(self):
        nonexisting_issue_url = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=0'
        with self.assertRaises(IssueDoesNotExistException):
            self.scraper.scrape(nonexisting_issue_url)

    def test_scrape_permission_denied_issue(self):
        permission_denied_url = 'https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=1'
        with self.assertRaises(IssuePermissionDeniedException):
            self.scraper.scrape(permission_denied_url)

    def test_get_project(self):
        project_1 = self.scraper._get_project(test_url_1)
        self.assertEqual(project_1, 'oss-fuzz')

        projzero_url = 'https://bugs.chromium.org/p/project-zero/issues/detail?id=2050&q=&can=1&sort=-id'
        project_projzero_url = self.scraper._get_project(projzero_url)
        self.assertEqual(project_projzero_url, 'project-zero')

    def test_get_issue_elem(self):
        # smoke test
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        self.assertIsNotNone(issue_elem_1)

    def test_get_left_column(self):
        # smoke test
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        left_col_1 = self.scraper._get_left_column(issue_elem_1)
        self.assertIsNotNone(left_col_1)

    def test_get_num_stars(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        left_col_1 = self.scraper._get_left_column(issue_elem_1)
        num_stars_1 = self.scraper._get_num_stars(left_col_1)
        # number of stars may change over time, so just sanity check the data
        self.assertGreaterEqual(num_stars_1, 0)

    def test_get_metadata(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        left_col_1 = self.scraper._get_left_column(issue_elem_1)
        metadata = self.scraper._get_metadata(left_col_1)
        self.assertEqual(len(metadata), 6)
        self.assertEqual(metadata['Owner'], '----')
        self.assertIn('amo...@gmail.com', metadata['CC'])
        self.assertIn('bug-binu...@gnu.org', metadata['CC'])
        self.assertIn('p.anto...@catenacyber.fr', metadata['CC'])
        self.assertIn('nickc@redhat.com', metadata['CC'])
        self.assertIsNotNone(metadata['Status']) # may change over time
        self.assertEqual(metadata['Components'], '----')
        self.assertIsNotNone(metadata['Modified']) # may change over time
        self.assertEqual(metadata['Type'], 'Bug')

    def test_get_labels(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        left_col_1 = self.scraper._get_left_column(issue_elem_1)
        labels = self.scraper._get_labels(left_col_1)
        self.assertEqual(len(labels), 8)
        self.assertIn('ClusterFuzz', labels)
        self.assertIn('Engine-libfuzzer', labels)
        self.assertIn('Reported-2020-01-10', labels)

    def test_get_right_column(self):
        # smoke test
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        self.assertIsNotNone(right_col_1)

    def test_get_header(self):
        # smoke test
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        self.assertIsNotNone(header_1)
        self.assertGreater(len(header_1.text), 0)

    def test_get_id(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        id_1 = self.scraper._get_id(header_1)
        self.assertEqual(id_1, 20000)

    def test_get_summary(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        summary_1 = self.scraper._get_summary(header_1)
        self.assertEqual(summary_1, 'binutils:fuzz_disassemble: Unsigned-integer-overflow in immediate')

    def test_get_author(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        author_1 = self.scraper._get_author(header_1)
        self.assertEqual(author_1, 'ClusterFuzz-External')

    def test_get_author_roles(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        author_roles_1 = self.scraper._get_author_roles(header_1)
        self.assertEqual(len(author_roles_1), 1)
        self.assertIn('Project Member', author_roles_1)

    def test_get_published(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        header_1 = self.scraper._get_header(right_col_1)
        published_1 = self.scraper._get_published(header_1)
        self.assertEqual(published_1.year, 2020)
        self.assertEqual(published_1.month, 1)
        # todo implement time-zone dependent day, hour and minute checks

    def test_get_issue_details(self):
        # smoke test
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        issue_details_1 = self.scraper._get_issue_details(right_col_1)
        self.assertIsNotNone(issue_details_1)

    def test_get_description(self):
        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        issue_details_1 = self.scraper._get_issue_details(right_col_1)
        description_1 = self.scraper._get_description(issue_details_1)
        # instead of checking against the whole text, just check the beginning, middle, and end.
        self.assertIn('Detailed', description_1)
        self.assertIn('Reproducer', description_1)
        self.assertIn('public.', description_1)

    def test_get_comments(self):
        # todo test for deleted comments

        issue_elem_1 = self.scraper._get_issue_elem(test_url_1)
        right_col_1 = self.scraper._get_right_column(issue_elem_1)
        issue_details_1 = self.scraper._get_issue_details(right_col_1)
        comments_1 = self.scraper._get_comments(issue_details_1)
        self.assertEqual(len(comments_1), 2)
        comment_1 = comments_1[0]
        self.assertEqual(comment_1.index, 1)
        self.assertEqual(comment_1.author, 'ClusterFuzz-External')
        self.assertEqual(len(comment_1.author_roles), 1)
        self.assertIn('Project Member', comment_1.author_roles)
        self.assertEqual(comment_1.published.year, 2020)
        self.assertEqual(comment_1.published.month, 1)
        # todo implement time-zone dependent day, hour and minute checks

        # instead of checking against the whole text, just check the beginning, middle, and end.
        self.assertIn('Status:', comment_1.issue_diff)
        self.assertIn('New)', comment_1.issue_diff)
        self.assertIn('ClusterFuzz-Verified', comment_1.issue_diff)

        self.assertIn('ClusterFuzz', comment_1.body)
        self.assertIn('If', comment_1.body)
        self.assertIn('https://github.com/google/oss-fuzz/issues/new', comment_1.body)
