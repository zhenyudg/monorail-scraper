from dataclasses import dataclass
from typing import Tuple

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass # essentially a struct
class OSSFuzzBugReport:
    project: str # software project in which a bug was found, not the same as Issue.project
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
