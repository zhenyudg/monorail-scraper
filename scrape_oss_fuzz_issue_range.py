import argparse

from typing import Tuple

from monorail_scraper.utils.scrape_util import scrape_issues


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
    scrape_issues('oss-fuzz', range(start, end + 1))


if __name__ == '__main__':
    main()
