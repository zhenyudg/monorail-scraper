from typing import Tuple


def get_args() -> Tuple[str, int]:
    import argparse

    parser = argparse.ArgumentParser(description='A web scraping tool for Monorail issue reports.')
    parser.add_argument('-p', '--project',  required=True, type=str,
                        help='The parent project of the issue to scrape. A list of projects is available at https://bugs.chromium.org/hosting/')
    parser.add_argument('-i', '--issue-id', required=True, type=int,
                        help='The ID of the issue to scrape.')

    args = parser.parse_args()

    return args.project, args.issue_id


def get_issue_url(project: str, issue_id: int) -> str:
    return 'https://bugs.chromium.org/p/{}/issues/detail?id={}'.format(project, issue_id)


def main():
    project, issue_id = get_args()
    issue_url = get_issue_url(project, issue_id)


if __name__ == '__main__':
    main()