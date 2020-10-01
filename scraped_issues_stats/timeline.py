import datetime
from pprint import pprint
from typing import Optional, Any, Tuple, Iterable

import numpy as np
import matplotlib.pyplot as plt

from issue.issue import Comment
from scraped_issues_stats.crash_type import group_by_crash_type
from scraped_issues_stats.utils import *


def get_verified_fix_notification_comment(oss_fuzz_issue: Issue) -> Optional[Comment]:
    """
    :param oss_fuzz_issue: An OSS-Fuzz bug issue
    :return: The fix verification comment (the newest if there are multiple such comments), or None
    if no such comment exists.
    """
    if oss_fuzz_issue.oss_fuzz_bug_report is None:
        raise ValueError("oss_fuzz_issue argument does not contain an .oss_fuzz_bug_report")
    if 'Verified' not in oss_fuzz_issue.metadata.get('Status', ''):
        return None

    verified_fix_comments = list()

    for comment in oss_fuzz_issue.comments:
        if comment.issue_diff is None:
            continue
        if 'Status: Verified' in comment.issue_diff:
            verified_fix_comments.append(comment)

    if len(verified_fix_comments) == 0:
        raise Warning(f"Issue {oss_fuzz_issue.id} has Verified status according to metadata, "
                      "but no fix verification comment was found.")

    # In most cases, there's only one comment that indicates a verified fix.
    # If there are more than one such comments (e.g., because a previously verified fix was actually incorrect),
    # then pick the most recent such comment.
    verified_fix_cmt = max(verified_fix_comments, key=lambda cmt: cmt.published)

    return verified_fix_cmt


def get_verified_fix_time(oss_fuzz_issue: Issue) -> Optional[datetime.datetime]:
    verified_fix_comment = get_verified_fix_notification_comment(oss_fuzz_issue)
    return None if verified_fix_comment is None else verified_fix_comment.published


def get_time_between_bug_found_and_fixed(oss_fuzz_issue: Issue) -> Optional[datetime.timedelta]:
    """
    :param oss_fuzz_issue: An OSS-Fuzz bug issue
    :return: The time elapsed (as a datetime.timedelta) between reporting a bug and verifying a patch,
    or None if the bug doesn't have a verified patch.
    """
    bug_found_time = oss_fuzz_issue.published
    bug_fixed_time = get_verified_fix_time(oss_fuzz_issue)
    if bug_fixed_time is None:
        return None
    else:
        return bug_fixed_time - bug_found_time


HumanReadableStats = Dict[str, Any]
UnfixedBugs = List[Issue]
BugTimedeltas = Dict[Issue, datetime.timedelta]
def get_fix_timeline_stats(oss_fuzz_issues: Iterable[Issue]) \
        -> Tuple[HumanReadableStats, UnfixedBugs, BugTimedeltas]:
    """
    :param oss_fuzz_issues: Iterable of OSS-Fuzz bug issues
    :return: Tuple containing:
    (Human readable statistics on the number and timelines of fixed bugs,
    Number of unfixed bugs,
    List of timedeltas between reporting and fixing a bug)
    """

    bugs_without_fix = list()
    bug_to_timedeltas = dict()

    for issue in oss_fuzz_issues:
        time_delta = get_time_between_bug_found_and_fixed(issue)
        if time_delta is None:
            bugs_without_fix.append(issue)
        else:
            bug_to_timedeltas[issue] = time_delta

    times_btw_bug_found_and_fixed = list(bug_to_timedeltas.values())

    if len(times_btw_bug_found_and_fixed) > 0:
        return {
            "bugs w/o a verified fix": len(bugs_without_fix),
            "bugs w/ a verified fix": len(times_btw_bug_found_and_fixed),
            "time between report and fix (min)": min(times_btw_bug_found_and_fixed),
            "time between report and fix (1st quantile)": np.quantile(times_btw_bug_found_and_fixed, 0.25),
            "time between report and fix (median)": np.median(times_btw_bug_found_and_fixed),
            "time between report and fix (3rd quantile)": np.quantile(times_btw_bug_found_and_fixed, 0.75),
            "time between report and fix (max)": max(times_btw_bug_found_and_fixed),
        }, bugs_without_fix, bug_to_timedeltas
    else:
        return {
            "bugs w/o a verified fix": len(bugs_without_fix),
            "bugs w/ a verified fix": len(times_btw_bug_found_and_fixed),
        }, bugs_without_fix, bug_to_timedeltas


def get_days_to_fix(oss_fuzz_issues: Iterable[Issue]) -> List[float]:
    """
    :param oss_fuzz_issues: Iterable of OSS-Fuzz issues
    :return: The number of days (can be fractional, e.g. 0.5 days) between bug reporting
    and a verified fix for each issue in oss_fuzz_issues.
    """
    timeline_stats, num_unfixed_bugs, bug_to_timedeltas = get_fix_timeline_stats(oss_fuzz_issues)
    timedeltas = bug_to_timedeltas.values()
    timedeltas_in_days = map(lambda tdelta: tdelta.total_seconds() / 86400, timedeltas)
    return list(timedeltas_in_days)


def generate_fix_timeline_visual(oss_fuzz_issues: Iterable[Issue]):
    timedelta_lists, labels = list(), list()

    # all bugs
    timedelta_lists.append(get_days_to_fix(oss_fuzz_issues))
    labels.append("all bugs")

    # security vulnerabilities
    sec_vulns = filter(lambda issue: issue.metadata['Type'] == 'Bug-Security', oss_fuzz_issues)
    timedelta_lists.append(get_days_to_fix(sec_vulns))
    labels.append('security vulnerabilities')

    # non-security bugs
    nonsec_bugs = filter(lambda issue: issue.metadata['Type'] == 'Bug', oss_fuzz_issues)
    timedelta_lists.append(get_days_to_fix(nonsec_bugs))
    labels.append('non-security bugs')

    # top N most common bug types
    N = 15
    bugs_by_crash_type = group_by_crash_type(oss_fuzz_issues)
    crash_types = list(bugs_by_crash_type.keys())
    crash_types.sort(key=lambda ct: -1 * len(bugs_by_crash_type[ct]))
    for i in range(N):
        crash_tp = crash_types[i]
        timedelta_lists.append(get_days_to_fix(bugs_by_crash_type[crash_tp]))
        labels.append(crash_tp)

    plt.boxplot(timedelta_lists, labels=labels)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Days between bug reported and bug patched")
    plt.yscale("log")

    plt.subplots_adjust(left=0.12, right=0.98, top=0.98, bottom=0.30)

    plt.savefig('timeline.jpg', dpi=250)


if __name__ == "__main__":
    oss_fuzz_issues = get_oss_fuzz_bug_reports(get_all_scraped_issues())
    generate_fix_timeline_visual(oss_fuzz_issues)
