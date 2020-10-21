import logging
import textwrap
import traceback
from typing import Iterable

from monorail_scraper.issue.issue_scraper import IssueScraper, get_issue_url, IssuePermissionDeniedException, \
    IssueDoesNotExistException, IssueDeletedException
from monorail_scraper.oss_fuzz.oss_fuzz_bug_report_parser import attach_oss_fuzz_bug_report


def scrape_issues(project: str, issues: Iterable[int]):
    issue_scraper = IssueScraper()

    print('[')

    is_first_successful_issue = True
    for i in issues:
        url_i = get_issue_url(project=project, issue_id=i)

        first_try, repeat_try = True, False
        while first_try or repeat_try:
            assert not (first_try and repeat_try)

            if first_try:
                page_loading_delay = 0.5
            else:
                page_loading_delay = 8

            try:
                issue_i = issue_scraper.scrape(url_i)
                attach_oss_fuzz_bug_report(issue_i)

                serialized_issue_i = issue_i.to_json(indent=4)
                serialized_issue_i = textwrap.indent(serialized_issue_i,
                                                     4 * ' ')  # indent entire serialization by 4 spaces

                if not is_first_successful_issue: print(',')
                is_first_successful_issue = False
                print(serialized_issue_i)

                first_try, repeat_try = False, False  # succeeded, don't try again
            except IssuePermissionDeniedException:
                logging.warning(f"Permission denied: issue {i}")
                first_try, repeat_try = False, False  # won't be successful, don't try again
            except IssueDoesNotExistException:
                logging.warning(f"Does not exist: issue {i}")
                first_try, repeat_try = False, False  # won't be successful, don't try again
            except IssueDeletedException:
                logging.warning(f"Deleted: issue {i}")
                first_try, repeat_try = False, False  # won't be successful, don't try again
            except Exception as e:
                # won't catch KeyboardInterrupt or SystemExit
                if first_try:
                    logging.warning(f"1st attempt failed: Exception encountered when parsing OSS-Fuzz issue {i}")
                    logging.warning(traceback.format_exc())

                    first_try = False
                    repeat_try = True  # try again, with a longer loading delay
                else:
                    logging.warning(f"2nd attempt failed: Exception encountered when parsing OSS-Fuzz issue {i}")
                    logging.warning(traceback.format_exc())

                    first_try, repeat_try = False, False  # give up, don't try again

    print(']')