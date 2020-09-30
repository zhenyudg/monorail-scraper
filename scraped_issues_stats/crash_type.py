import matplotlib.pyplot as plt

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

    # empty string crash type is unknown
    if crash_type == '':
        return 'unknown'

    ambiguous_signal_crash_types = ['unknown signal', 'fatal signal']
    if crash_type in ambiguous_signal_crash_types:
        return f'signal: unknown'

    signal_crash_types = ['abrt', 'bus', 'ill']
    if crash_type in signal_crash_types:
        return f'signal: {crash_type}'

    if 'timeout' in crash_type:
        return 'timeout'

    if 'out of memory' in crash_type:
        return 'out of memory'

    # Go is memory safe, so bad indexing shouldn't lead to buffer overflows
    if crash_type == 'index out of range':
        return 'index out of range in Go'

    # Normalize the flavors (heap, stack, global) of buffer overflows
    # Keep overflow reads and writes separate due to differing security impacts
    # UBSAN's index out of bounds doesn't specify whether it's read or write
    if crash_type == 'index out of bounds':
        return 'buffer overflow static bounds'
    if 'buffer' in crash_type and ('overflow' in crash_type or 'underflow' in crash_type):
        if 'read' in crash_type:
            return 'buffer overflow read'
        elif 'write' in crash_type:
            return 'buffer overflow write'
        else:
            return 'buffer overflow unknown'

    if crash_type == 'direct leak' or crash_type == 'indirect leak':
        return 'leak'

    if 'integer overflow' in crash_type:
        return 'integer overflow'

    if 'divide by zero' in crash_type:
        return 'divide by zero'

    # Normalize between read/write null dereferences
    if 'null dereference' in crash_type or 'null reference' in crash_type:
        return 'null dereference'

    # catch all case
    return crash_type


def group_by_crash_type(oss_fuzz_bugs: OSSFuzzBugIssues) -> Dict[CrashType, Collection[Issue]]:
    return group_by(oss_fuzz_bugs,
                    lambda issue: preprocess_crash_type(issue.oss_fuzz_bug_report.crash_type))


def generate_crash_type_visual(oss_fuzz_bugs: OSSFuzzBugIssues):
    from scraped_issues_stats.timeline import get_fix_timeline_stats
    nums_unfixed_bugs: List[int] = list()
    nums_fixed_bugs: List[int] = list()
    xlabels: List[str] = list()

    bugs_by_crash_type = group_by_crash_type(oss_fuzz_bugs)
    crash_types = list(bugs_by_crash_type.keys())
    crash_types.sort(key=lambda ct: -1 * len(bugs_by_crash_type[ct]))

    # keep the top N most common crash types, aggregate the rest
    N = 15
    other_crash_types = crash_types[N:]
    bugs_with_other_ct: List[Issue] = list()
    for other_ct in other_crash_types:
        bugs_with_other_ct.extend(bugs_by_crash_type[other_ct])
        del bugs_by_crash_type[other_ct]
        crash_types.remove(other_ct)
    bugs_by_crash_type['other'] = bugs_with_other_ct
    crash_types.append('other')

    for crash_tp in crash_types:
        bugs = bugs_by_crash_type[crash_tp]
        n_bugs = len(bugs)
        unfixed_bugs = get_fix_timeline_stats(bugs)[1]
        n_unfixed_bugs = len(unfixed_bugs)
        n_fixed_bugs = n_bugs - n_unfixed_bugs
        nums_unfixed_bugs.append(n_unfixed_bugs)
        nums_fixed_bugs.append(n_fixed_bugs)
        xlabels.append(crash_tp)

    # make the bar graph
    fixed_bars = plt.bar(xlabels, nums_fixed_bugs)
    unfixed_bars = plt.bar(xlabels, nums_unfixed_bugs, bottom=nums_fixed_bugs)
    plt.ylabel('Number of bugs')
    plt.xticks(rotation=30, ha='right')
    plt.legend((fixed_bars, unfixed_bars), ("Fixed", "Unfixed"))

    # add exact numbers
    # fixed bugs
    for bar in fixed_bars:
        bar_x = bar.get_x()
        bar_ytop = bar.get_height()
        num_fixed = bar_ytop
        plt.text(bar_x, bar_ytop - 50, num_fixed, fontsize=8)
    # total bugs (fixed + unfixed)
    for bar in unfixed_bars:
        bar_x = bar.get_x()
        bar_ytop = bar.get_y() + bar.get_height()
        num_total = bar_ytop
        num_unfixed = bar.get_height()
        plt.text(bar_x, bar_ytop + 20, num_total, fontsize=8)

    plt.subplots_adjust(left=0.11, right=0.98, top=0.98, bottom=0.25)

    plt.show()


if __name__ == '__main__':
    issues = get_all_scraped_issues()
    oss_fuzz_bugs = get_oss_fuzz_bug_reports(issues)
    generate_crash_type_visual(oss_fuzz_bugs)
