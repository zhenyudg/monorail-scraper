import argparse
import logging
import textwrap
import traceback

from typing import Tuple

from issue.issue_scraper import get_issue_url, IssueScraper, ScrapeException
from oss_fuzz.oss_fuzz_bug_report_parser import attach_oss_fuzz_bug_report


def get_args() -> Tuple[int, int]:
    parser = argparse.ArgumentParser(description='Scrapes a range of OSS-Fuzz issues, '
                                                 'and outputs serialized issues to stdout')
    parser.add_argument('-s', '--start', required=True, type=int,
                        help='Starting OSS-Fuzz issue number (inclusive).')
    parser.add_argument('-e', '--end', required=True, type=int,
                        help='Ending OSS-Fuzz issue number (inclusive).')

    args = parser.parse_args()

    start = args.start
    end = args.end

    # ensure that start <= end
    if start > end:
        start, end = end, start

    return start, end


def main():
    start, end = get_args()
    issue_scraper = IssueScraper()

    print('[')

    for i in range(start, end+1):
        url_i = get_issue_url(project='oss-fuzz', issue_id=i)
        try:
            issue_i = issue_scraper.scrape(url_i)
            attach_oss_fuzz_bug_report(issue_i)

            serialized_issue_i = issue_i.to_json(indent=4)
            serialized_issue_i = textwrap.indent(serialized_issue_i, 4 * ' ') # indent entire serialization by 4 spaces

            if i > start: print(',')
            print(serialized_issue_i)
        except Exception as e:
            # won't catch KeyboardInterrupt or SystemExit
            logging.error(f"Exception encountered when parsing OSS-Fuzz issue {i}\n")
            logging.error(traceback.format_exc())

    print(']')


if __name__ == '__main__':
    main()
