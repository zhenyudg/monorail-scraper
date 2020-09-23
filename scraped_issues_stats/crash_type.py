from scraped_issues_stats.utils import *

CrashType = str
def preprocess_crash_type(raw_crash_type: str) -> CrashType:
    # Normalize case and separator token (use spaces instead of dashes).
    crash_type = raw_crash_type.lower().replace('-', ' ')

    # remove numerical or '{*}' suffixes
    parts = crash_type.rsplit(' ', 1)
    if len(parts) > 1:
        last_part = parts[-1]
        if last_part == '{*}' or last_part.isnumeric():
            crash_type = parts[0]

    signal_crash_types = ['abrt', 'bus', 'ill', 'unknown signal']
    if crash_type in signal_crash_types:
        return f'signal: {crash_type}'

    if 'timeout' in crash_type:
        return 'timeout'

    if 'out of memory' in crash_type:
        return 'out of memory'

    # Normalize the flavors (heap, stack, global) of buffer overflows
    # Keep overflow reads and writes separate due to differing security impacts
    if 'buffer' in crash_type and ('overflow' in crash_type or 'underflow' in crash_type):
        if 'read' in crash_type:
            return 'buffer overflow read'
        if 'write' in crash_type:
            return 'buffer overflow write'

    if crash_type == 'direct leak' or crash_type == 'indirect leak':
        return 'leak'

    if 'integer overflow' in crash_type:
        return 'integer overflow'

    if 'divide by zero' in crash_type:
        return 'divide by zero'

    # Normalize between read/write null dereferences
    if 'null dereference' in crash_type:
        return 'null dereference'

    # catch all case
    return crash_type


def group_by_crash_type(oss_fuzz_bugs: OSSFuzzBugReports) -> Dict[CrashType, Collection[Issue]]:
    return group_by(oss_fuzz_bugs,
                    lambda issue: preprocess_crash_type(issue.oss_fuzz_bug_report.crash_type))


if __name__ == '__main__':
    issues = get_all_scraped_issues()
    oss_fuzz_bugs = get_oss_fuzz_bug_reports(issues)
    bugs_by_crash_type = group_by_crash_type(oss_fuzz_bugs)
    crash_types = list(bugs_by_crash_type.keys())
    crash_types.sort(key=lambda ct: -1 * len(bugs_by_crash_type[ct]))
    for ct in crash_types: print(ct, '|', len(bugs_by_crash_type[ct]))
