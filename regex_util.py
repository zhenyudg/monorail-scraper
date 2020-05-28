import re


def capture(input: str, regex: str, pattern_flags: int = 0, groupnum: int = 1) -> str:
    pattern = re.compile(regex, pattern_flags)
    match = pattern.search(input)
    captured_text = match.group(groupnum)
    return captured_text