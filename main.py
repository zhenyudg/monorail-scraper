from typing import Tuple

from issue_scraper import IssueScraper, get_issue_url
from oss_fuzz.oss_fuzz_bug_report_parser import attach_oss_fuzz_bug_report


def get_args() -> Tuple[str, int]:
    import argparse

    parser = argparse.ArgumentParser(description='A web scraping tool for Monorail issue reports.')
    parser.add_argument('-p', '--project',  required=True, type=str,
                        help='The parent project of the issue to scrape. A list of projects is available at https://bugs.chromium.org//')
    parser.add_argument('-i', '--issue-id', required=True, type=int,
                        help='The ID of the issue to scrape.')

    args = parser.parse_args()

    return args.project, args.issue_id


def main():
    project, issue_id = get_args()
    issue_url = get_issue_url(project, issue_id)
    issue_scraper = IssueScraper()
    issue = issue_scraper.scrape(issue_url)

    attach_oss_fuzz_bug_report(issue)

    output = issue.to_json(indent=4)
    print(output)


if __name__ == '__main__':
    main()
