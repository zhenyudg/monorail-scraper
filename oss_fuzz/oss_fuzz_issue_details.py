from dataclasses import dataclass
from typing import Tuple


@dataclass # essentially a struct
class OSSFuzzIssueDetails:
    project: str
    fuzzing_engine: str
    fuzz_target_binary: str
    job_type: str
    platform_id: str
    crash_type: str
    crash_addr: str
    crash_state: Tuple[str, ...]
    sanitizer: str
    regressed_commits_url: str
    fixed_commits_url: str
    testcase_url: str