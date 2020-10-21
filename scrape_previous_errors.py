import argparse
import re
from typing import Tuple, List

from monorail_scraper.utils.scrape_util import scrape_issues

ErrReportPath = str
RescrapePermissionDeniedErrs = bool
def get_args() -> Tuple[ErrReportPath, RescrapePermissionDeniedErrs]:
    parser = argparse.ArgumentParser(description='Re-scrape OSS-Fuzz issues that failed previously')
    parser.add_argument('err_report_path',
                        help='File containing error messages from a previous scraping attempt')
    parser.add_argument('--rescrape_perm_denied_errs', action='store_true',
                        help='Rescrape issues where permission was previously denied')

    args = parser.parse_args()

    return args.err_report_path, args.rescrape_perm_denied_errs


IssueID = int
def get_issues_to_rescrape(err_report_path: str, rescrape_perm_denied_errs: bool) -> List[int]:
    with open(err_report_path) as f:
        err_report = f.read()

    err_ptrn = re.compile(r'WARNING:root:2nd attempt failed: Exception encountered when parsing OSS-Fuzz issue ([0-9]+)')
    ids = err_ptrn.findall(err_report)

    if rescrape_perm_denied_errs:
        perm_ptrn = re.compile(r'WARNING:root:Permission denied: issue ([0-9]+)')
        perm_ids = perm_ptrn.findall(err_report)
        ids += perm_ids

    # convert strings to ints, then sort
    ids = [int(id) for id in ids]
    ids.sort()

    return ids


if __name__ == '__main__':
    err_report_path, rescrape_perm_denied_errs = get_args()
    issues = get_issues_to_rescrape(err_report_path, rescrape_perm_denied_errs)
    scrape_issues('oss-fuzz', issues)
