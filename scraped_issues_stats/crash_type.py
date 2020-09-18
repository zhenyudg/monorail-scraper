from scraped_issues_stats.utils import *

CrashType = str
def preprocess_crash_type(raw_crash_type: str) -> CrashType:
    if 'Timeout' in raw_crash_type:
        return 'Timeout'
    if 'Out-of-memory' in raw_crash_type:
        return 'Out-of-memory'
    if 'Stack overflow' == raw_crash_type:
        return 'Stack-overflow'

    parts = raw_crash_type.rsplit(' ', 1)
    if len(parts) <= 1:
        return raw_crash_type
    else:
        last_part = parts[-1]
        if last_part == '{*}' or last_part.isnumeric():
            return parts[0]
        else:
            return raw_crash_type


def group_by_crash_type(oss_fuzz_bugs: OSSFuzzBugReports) -> Dict[CrashType, Collection[Issue]]:
    return group_by(oss_fuzz_bugs,
                    lambda issue: preprocess_crash_type(issue.oss_fuzz_bug_report.crash_type))


if __name__ == '__main__':
    issues = get_all_scraped_issues()
    oss_fuzz_bugs = get_oss_fuzz_bug_reports(issues)
    bugs_by_crash_type = group_by_crash_type(oss_fuzz_bugs)
    crash_types = list(bugs_by_crash_type.keys())
    crash_types.sort()
    for ct in crash_types: print(ct, '|', len(bugs_by_crash_type[ct]))
