from typing import Tuple, Collection, Optional

import re

from issue import Comment, Issue

# minimum issue number: 5 (anything lower is not publically accessible)
# maximum issue number at time of writing: 22411

# +? and *? are the non-greedy versions of + and *; they match minimally instead of maximally
# Use [\n$] when possible for forwards compatibility if & when we switch to shadow DOM parsing

# Reason to keep parsing functions as 'top-level' functions:
# None (todo: consider a refactor)
from oss_fuzz.oss_fuzz_bug_report import OSSFuzzBugReport
from string_util import capture


def parse_oss_fuzz_issue_details(issue: Issue) -> OSSFuzzBugReport:
    id = issue.id
    description = issue.description
    comments = issue.comments

    project = get_project(description, id)
    fuzzing_engine = get_fuzzing_engine(description, id)
    fuzz_target_binary = get_fuzz_target_binary(description, id)
    job_type = get_job_type(description)
    platform_id = get_platform_id(description)
    crash_type = get_crash_type(description)
    crash_addr = get_crash_address(description)
    crash_state = get_crash_state(description)
    sanitizer = get_sanitizer(description, id)
    regressed_commits_url = get_regressed_commits_url(description)
    fixed_commits_url = get_fixed_commits_url(comments, id)
    testcase_url = get_testcase_url(description, id)

    oss_fuzz_issue_details = OSSFuzzBugReport(project=project, fuzzing_engine=fuzzing_engine,
                                              fuzz_target_binary=fuzz_target_binary, job_type=job_type,
                                              platform_id=platform_id, crash_type=crash_type, crash_addr=crash_addr,
                                              crash_state=crash_state, sanitizer=sanitizer,
                                              regressed_commits_url=regressed_commits_url,
                                              fixed_commits_url=fixed_commits_url, testcase_url=testcase_url)

    return oss_fuzz_issue_details


def get_project(description: str, id: int) -> str:
    if id <= 135:
        # todo: parse projects from "Job Type: " or title
        raise NotImplementedError("Issues <= 135 not supported")
    elif 135 <= id <= 212:
        return capture(description, r'Target: (.+?)[\n$]')
    else: # issue_num >= 213
        return capture(description, r'Project: (.+?)[\n$]')


def get_fuzzing_engine(description: str, id: int) -> str:
    if id <= 16307:
        jobtype = capture(description, r'Job Type: (.+?)[\n$]')
        if jobtype.startswith('afl'):
            return 'afl'
        elif jobtype.startswith('libfuzzer'):
            return 'libFuzzer'
        elif jobtype.startswith('honggfuzz'):
            # there aren't any issues w/ id <= 16307 that featured honggfuzz
            return 'honggfuzz'
        else:
            # any fuzz engines that I missed
            return jobtype.split('_')[0]
    elif id >= 16308:
        return capture(description, r'Fuzzing Engine: (.+?)[\n$]')


def get_fuzz_target_binary(description: str, id: int) -> str:
    if id <= 251:
        # todo: heuristically find fz tgt by stripping the fuzz engine prefix off of the "Fuzzer: " field
        raise NotImplementedError("Issues <= 251 not supported")
    elif 252 <= id <= 16307:
        return capture(description, r'Fuzz target binary: (.+?)[\n$]')
    elif id >= 16308:
        return capture(description, r'Fuzz Target: (.+?)[\n$]')


def get_job_type(description: str) -> str:
    return capture(description, r'Job Type: (.+?)[\n$]')


def get_platform_id(description: str) -> str:
    return capture(description, r'Platform Id: (.+?)[\n$]')


def get_crash_type(description: str) -> str:
    return capture(description, r'Crash Type: (.+?)[\n$]')


def get_crash_address(description: str) -> str:
    # There might not be the address; in that case, capture the empty string
    return capture(description, r'Crash Address: (.*?)[\n$]')


def get_crash_state(description: str) -> Tuple[str]:
    # The . qualifier doesn't match \n by default
    raw_crash_state = capture(description, r'Crash State:\n(.*?)\n  \n', pattern_flags=re.DOTALL)

    lines = raw_crash_state.split('\n')
    crash_state = list()
    for line in lines:
        cleaned_line = line.strip()
        if len(cleaned_line) > 0:
            crash_state.append(cleaned_line)

    return tuple(crash_state)


def get_sanitizer(description: str, id: int) -> str:
    if id <= 383:
        #todo: parse from job type
        raise NotImplementedError("Issues <= 383 not supported")
    elif id >= 384:
        return capture(description, r'Sanitizer: (.+?)[\n$]')


def get_regressed_commits_url(description: str) -> str:
    # almost all issues have urls to regression commits, except a handful of extremely old issues
    pattern = re.compile(r'Regressed: (.+?)[\n$]')
    match = pattern.search(description)
    if match is not None:
        regressed = match.group(1)
    else: # no match
        regressed = None
    return regressed


def get_fixed_commits_url(comments: Collection[Comment], id: int) -> Optional[str]:
    if id <= 14834:
        regex = r'Fixed: (.+?)[\n$]'
    else: # id >= 14835
        regex = r'ClusterFuzz testcase [0-9]+ is verified as fixed in (.+?)[\n$]'
    pattern = re.compile(regex)
    fixed_commits_url = None

    for comment in comments:
        if comment.author != 'ClusterFuzz-External':
            continue

        match = pattern.search(comment.body)
        if match is None:
            continue

        fixed_commits_url = match.group(1)
        break

    return fixed_commits_url


def get_testcase_url(description: str, id: int) -> str:
    if id <= 125:
        return capture(description, r'Download: (.+?)[\n$]')
    elif 126 <= id <= 500:
        return capture(description, r'Minimized Testcase \(.+?\): (.+?)[\n$]')
    elif id >= 501:
        return capture(description, r'Reproducer Testcase: (.+?)[\n$]')


def get_report_date(raw_text: str) -> str:
    return capture(raw_text, r'Reported by ClusterFuzz-External on (.+?) Project Member [\n$]')
