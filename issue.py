import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Comment:
    index: int
    author: str
    author_roles: List[str]
    published: datetime.datetime
    issue_diff: Optional[str]
    body: str


@dataclass # essentially a struct
class Issue:
    retrieved: datetime.datetime # time when the issue was scraped
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
    additional_info: Optional[Any] = None # currently used for OSSFuzzIssueDetails