from typing import Tuple

import re
from dataclasses import dataclass

from issue_scraper import Issue

# minimum issue number: 5 (anything lower is not publically accessible)
# maximum issue number at time of writing: 22411

# +? and *? are the non-greedy versions of + and *; they match minimally instead of maximally
# Use [\n$] when possible for forwards compatibility if & when we switch to shadow DOM parsing

# Reason to keep parsing functions as 'top-level' functions:
# There's a high chance that we'll repurpose them to parse data from shadow DOMs.
# In that case, the raw_text argument won't all be the same.


@dataclass # essentially a struct
class OSSFuzzIssue(Issue):
    project: str
    fuzzing_engine: str
    fuzz_target_binary: str
    job_type: str
    platform_id: str
    crash_type: str
    crash_addr: str
    crash_state: Tuple[str]
    sanitizer: str
    regressed_commits_url: str
    fixed_commits_url: str
    testcase_url: str


def capture(input: str, regex: str, pattern_flags: int = 0, groupnum: int = 1) -> str:
    pattern = re.compile(regex, pattern_flags)
    match = pattern.search(input)
    captured_text = match.group(groupnum)
    return captured_text


def get_issue_num(raw_text: str) -> int:
    return int(capture(raw_text, r'Issue ([0-9]+?):'))


def get_title(raw_text: str) -> str:
    return capture(raw_text, r'Issue [0-9]+?: (.+?)[\n$]')


def get_project(raw_text: str, issue_num: int) -> str:
    if issue_num <= 135:
        # todo: parse projects from "Job Type: " or title
        raise NotImplementedError("Issues <= 135 not supported")
    elif 135 <= issue_num <= 212:
        return capture(raw_text, r'Target: (.+?)[\n$]')
    else: # issue_num >= 213
        return capture(raw_text, r'Project: (.+?)[\n$]')


def get_fuzzing_engine(raw_text: str, issue_num: int) -> str:
    if issue_num <= 16307:
        # todo: heuristically figure out the fuzzing engine by checking for known fuzz engines in the text
        # todo: it's probably in the "Fuzzer: " field
        raise NotImplementedError("Issues <= 16307 not supported")
    elif issue_num >= 16308:
        return capture(raw_text, r'Fuzzing Engine: (.+?)[\n$]')


def get_fuzz_target_binary(raw_text: str, issue_num: int) -> str:
    if issue_num <= 251:
        # todo: heuristically find fz tgt by stripping the fuzz engine prefix off of the "Fuzzer: " field
        raise NotImplementedError("Issues <= 251 not supported")
    elif 252 <= issue_num <= 16307:
        return capture(raw_text, r'Fuzz target binary: (.+?)[\n$]')
    elif issue_num >= 16308:
        return capture(raw_text, r'Fuzz Target: (.+?)[\n$]')


def get_job_type(raw_text: str) -> str:
    return capture(raw_text, r'Job Type: (.+?)[\n$]')


def get_platform_id(raw_text: str) -> str:
    return capture(raw_text, r'Platform Id: (.+?)[\n$]')


def get_crash_type(raw_text: str) -> str:
    return capture(raw_text, r'Crash Type: (.+?)[\n$]')


def get_crash_address(raw_text: str) -> str:
    # There might not be the address; in that case, capture the empty string
    return capture(raw_text, r'Crash Address: (.*?)[\n$]')


def get_crash_state(raw_text: str) -> Tuple[str]:
    # If/when I mine using shadow DOMs, look for an empty span with no content after the crash state's lines

    # The . qualifier doesn't match \n by default
    raw_crash_state = capture(raw_text, r'Crash State:\n(.*?)\n  \n', pattern_flags=re.DOTALL)

    lines = raw_crash_state.split('\n')
    crash_state = list()
    for line in lines:
        cleaned_line = line.strip()
        if len(cleaned_line) > 0:
            crash_state.append(cleaned_line)

    return tuple(crash_state)


def get_sanitizer(raw_text: str, issue_num: int) -> str:
    if issue_num <= 383:
        #todo: parse from job type
        raise NotImplementedError("Issues <= 383 not supported")
    elif issue_num >= 384:
        return capture(raw_text, r'Sanitizer: (.+?)[\n$]')


def get_regressed_commits_url(raw_text: str) -> str:
    # almost all issues have urls to regression commits, except a handful of extremely old issues
    pattern = re.compile(r'Regressed: (.+?)[\n$]')
    match = pattern.search(raw_text)
    if match is not None:
        regressed = match.group(1)
    else: # no match
        regressed = None
    return regressed


def get_fixed_commits_url(raw_text: str, issue_num: int) -> str:
    if issue_num <= 14834:
        return capture(raw_text, r'Fixed: (.+?)[\n$]')
    elif issue_num >= 14835:
        return capture(raw_text, r'ClusterFuzz testcase [0-9]+ is verified as fixed in (.+?)[\n$]')


def get_testcase_url(raw_text: str, issue_num: int) -> str:
    if issue_num <= 125:
        return capture(raw_text, r'Download: (.+?)[\n$]')
    elif 126 <= issue_num <= 500:
        return capture(raw_text, r'Minimized Testcase \(.+?\): (.+?)[\n$]')
    elif issue_num >= 501:
        return capture(raw_text, r'Reproducer Testcase: (.+?)[\n$]')


def get_report_date(raw_text: str) -> str:
    return capture(raw_text, r'Reported by ClusterFuzz-External on (.+?) Project Member [\n$]')
