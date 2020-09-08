from typing import Tuple, Collection, Optional

from issue.issue import Comment, Issue

# minimum issue number: 5 (anything lower is not publically accessible)
# maximum issue number at time of writing: 22411

# +? and *? are the non-greedy versions of + and *; they match minimally instead of maximally
# Use [\n$] when possible for forwards compatibility if & when we switch to shadow DOM parsing

# Reason to keep parsing functions as 'top-level' functions:
# None (todo: consider a refactor)
from oss_fuzz.oss_fuzz_bug_report import OSSFuzzBugReport
from utils.string_util import *


def attach_oss_fuzz_bug_report(issue: Issue) -> bool:
    """
    Attaches an OSS-Fuzz bug report to an issue if the issue indeed contains an
    OSS-Fuzz bug report (checked with is_oss_fuzz_bug_report()).

    :param issue: The issue to attach an OSSFuzzBugReport to. Will be modified in-place --- the
    Issue.oss_fuzz_bug_report will be filled.
    :return: whether an OSSFuzzBugReport was successfully attached to issue. If True, then
    issue was modified in-place. If False, then issue was unchanged.
    """
    if not is_oss_fuzz_bug_report(issue):
        return False
    else:
        report = parse_oss_fuzz_bug_report_details(issue)
        issue.oss_fuzz_bug_report = report
        return True


def is_oss_fuzz_bug_report(issue: Issue) -> bool:
    is_oss_fuzz = almost_equal("oss-fuzz", issue.project)
    if not is_oss_fuzz:
        return False
    else:
        is_nonsecurity_bug_report = almost_equal("Bug", issue.metadata['Type'])
        is_security_bug_report = almost_equal("Bug-Security", issue.metadata['Type'])
        return is_nonsecurity_bug_report or is_security_bug_report


def parse_oss_fuzz_bug_report_details(issue: Issue) -> OSSFuzzBugReport:
    id = issue.id
    description = issue.description
    comments = issue.comments

    project = _get_project(description, id)
    fuzzing_engine = _get_fuzzing_engine(description, id)
    fuzz_target_binary = _get_fuzz_target_binary(description, id)
    job_type = _get_job_type(description)
    platform_id = _get_platform_id(description)
    crash_type = _get_crash_type(description)
    crash_addr = _get_crash_address(description)
    crash_state = _get_crash_state(description)
    sanitizer = _get_sanitizer(description, id)
    regressed_commits_url = _get_regressed_commits_url(description)
    fixed_commits_url = _get_fixed_commits_url(comments, id)
    testcase_url = _get_testcase_url(description, id)

    oss_fuzz_issue_details = OSSFuzzBugReport(project=project, fuzzing_engine=fuzzing_engine,
                                              fuzz_target_binary=fuzz_target_binary, job_type=job_type,
                                              platform_id=platform_id, crash_type=crash_type, crash_addr=crash_addr,
                                              crash_state=crash_state, sanitizer=sanitizer,
                                              regressed_commits_url=regressed_commits_url,
                                              fixed_commits_url=fixed_commits_url, testcase_url=testcase_url)

    return oss_fuzz_issue_details


def _get_jobtype(description: str) -> str:
    return capture(description, r'Job Type: (.+?)[\n$]')


def _get_project(description: str, id: int) -> str:
    if id <= 135:
        jobtype = _get_jobtype(description)
        project = jobtype.strip().split('_')[-1]
        return project
    elif 135 <= id <= 212:
        return capture(description, r'Target: (.+?)[\n$]')
    else: # issue_num >= 213
        return capture(description, r'Project: (.+?)[\n$]')


def _get_fuzzing_engine(description: str, id: int) -> str:
    if id <= 16307:
        jobtype = _get_jobtype(description)
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


def _get_fuzz_target_binary(description: str, id: int) -> str:
    if id <= 251:
        fuzzer = capture(description, r'Fuzzer: (.+?)[\n$]')
        fuzz_target_binary = fuzzer.split('_', maxsplit=1)[1]
        return fuzz_target_binary
    elif 252 <= id <= 16307:
        return capture(description, r'Fuzz target binary: (.+?)[\n$]')
    elif id >= 16308:
        return capture(description, r'Fuzz Target: (.+?)[\n$]')


def _get_job_type(description: str) -> str:
    return capture(description, r'Job Type: (.+?)[\n$]')


def _get_platform_id(description: str) -> str:
    return capture(description, r'Platform Id: (.+?)[\n$]')


def _get_crash_type(description: str) -> str:
    return capture(description, r'Crash Type: (.+?)[\n$]')


def _get_crash_address(description: str) -> str:
    # There might not be the address; in that case, capture the empty string
    return capture(description, r'Crash Address: (.*?)[\n$]')


def _get_crash_state(description: str) -> Tuple[str]:
    # The . qualifier doesn't match \n by default
    raw_crash_state = capture(description, r'Crash State:\n(.*?)\n  \n', pattern_flags=re.DOTALL)

    lines = raw_crash_state.split('\n')
    crash_state = list()
    for line in lines:
        cleaned_line = line.strip()
        if len(cleaned_line) > 0:
            crash_state.append(cleaned_line)

    return tuple(crash_state)


def _get_sanitizer(description: str, id: int) -> str:
    if id <= 383:
        jobtype = capture(description, r'Job Type: (.+?)[\n$]')
        return _get_sanitizer_from_jobtype(jobtype)
    elif id >= 384:
        return capture(description, r'Sanitizer: (.+?)[\n$]')


def _get_sanitizer_from_jobtype(jobtype: str) -> str:
    jobtype_words = jobtype.split('_')
    for word in jobtype_words:
        if almost_equal(word, 'asan'):
            return "address (ASAN)"
        elif almost_equal(word, 'ubsan'):
            return "undefined (UBSAN)"
        elif almost_equal(word, 'msan'):
            return "memory (MSAN)"
        elif almost_equal(word, 'tsan'):
            return "thread (TSAN)"
        elif almost_equal(word, 'lsan'):
            return "leak (LSAN)"

    # no sanitizer found
    return ''


def _get_regressed_commits_url(description: str) -> Optional[str]:
    # almost all issues have urls to regression commits, except a handful of extremely old issues
    pattern = re.compile(r'Regressed: (.+?)[\n$]')
    match = pattern.search(description)
    if match is not None:
        regressed = match.group(1)
    else: # no match
        regressed = None
    return regressed


def _get_fixed_commits_url(comments: Collection[Comment], id: int) -> Optional[str]:
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


def _get_testcase_url(description: str, id: int) -> str:
    if id <= 125:
        return capture(description, r'Download: (.+?)[\n$]')
    elif 126 <= id <= 500:
        return capture(description, r'Minimized Testcase \(.+?\): (.+?)[\n$]')
    elif id >= 501:
        return capture(description, r'Reproducer Testcase: (.+?)[\n$]')


def _get_report_date(raw_text: str) -> str:
    return capture(raw_text, r'Reported by ClusterFuzz-External on (.+?) Project Member [\n$]')
