import re


def capture(input: str, regex: str, pattern_flags: int = 0, groupnum: int = 1) -> str:
    pattern = re.compile(regex, pattern_flags)
    match = pattern.search(input)
    captured_text = match.group(groupnum)
    return captured_text


def almost_equal(str1: str, str2: str) -> bool:
    if str1 is None or str2 is None:
        return str1 is None and str2 is None
    else:
        str1_processed = re.sub(r'\W+', '', str1.strip().casefold())
        str2_processed = re.sub(r'\W+', '', str2.strip().casefold())
        return str1_processed == str2_processed
