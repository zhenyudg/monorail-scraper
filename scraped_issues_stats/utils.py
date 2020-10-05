import logging
import os
import pickle

import ujson

from pathlib import Path
from typing import List, NewType, Collection, Callable, Dict

from monorail_scraper.issue.issue import Issue

AllScrapedIssues = NewType('AllScrapedIssues', List[Issue])
OSSFuzzBugIssues = NewType('OSSFuzzBugIssues', List[Issue])


def get_all_scraped_issues(scraped_issues_dir: str = '../scraped_issues') -> AllScrapedIssues:
    issues: List[Issue] = list()

    cached_issues_path = f'{scraped_issues_dir}/cache.pickle'
    if os.path.isfile(cached_issues_path):
        with open(cached_issues_path, 'rb') as f:
            issues = pickle.load(f)
            logging.warning('Done retrieving serialized issues from cache.')
            return AllScrapedIssues(issues)

    # no cached issues, load from json instead
    for issues_filepath_i in Path(scraped_issues_dir).rglob('*.json'):
        logging.warning(f'Loading {issues_filepath_i}')

        issues_file_i = open(issues_filepath_i)
        issues_i = ujson.load(issues_file_i)
        for issue_dict in issues_i:
            issue = Issue.from_dict(issue_dict)
            issues.append(issue)

    with open(cached_issues_path, 'wb') as f:
        pickle.dump(issues, f)

    logging.warning('Done retrieving serialized issues.')
    return AllScrapedIssues(issues)


def get_oss_fuzz_bug_reports(all_scraped_issues: AllScrapedIssues) -> OSSFuzzBugIssues:
    oss_fuzz_issues = list(filter(lambda issue: issue.oss_fuzz_bug_report is not None, all_scraped_issues))
    return OSSFuzzBugIssues(oss_fuzz_issues)


Feature = any
def group_by(issues: Collection[Issue], fn_get_feature: Callable[[Issue], Feature]) \
    -> Dict[Feature, Collection[Issue]]:
    categorization = dict()

    for issue in issues:
        feature = fn_get_feature(issue)
        if feature not in categorization.keys():
            categorization[feature] = list()
        categorization[feature].append(issue)

    return categorization


def percent(n, d) -> str:
    return f'{round(n/d * 100)}%'
