import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict

from dataclasses_json import dataclass_json

from oss_fuzz.oss_fuzz_bug_report import OSSFuzzBugReport


@dataclass_json
@dataclass
class Comment:
    index: int
    author: str
    author_roles: List[str]
    published: datetime.datetime
    issue_diff: Optional[str]
    body: str


@dataclass_json
@dataclass
class Issue:
    retrieved: datetime.datetime # time when the issue was scraped
    project: str
    id: int
    summary: str # summary = title
    author: str
    author_roles: List[str]
    published: datetime.datetime
    stars: int
    metadata: Dict[str, str]
    labels: List[str]
    description: str # description = main text
    comments: List[Comment]

    oss_fuzz_bug_report: Optional[OSSFuzzBugReport] = None
