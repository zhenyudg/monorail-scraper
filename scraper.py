import datetime
import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Collection

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver


@dataclass
class Comment:
    index: int
    author: str
    author_role: Optional[str]
    published: datetime.datetime
    issue_diff: Optional[Dict[str, str]]
    body: str


@dataclass # essentially a struct
class Issue:
    retrieved: datetime.datetime # time when the issue was scraped
    id: int
    summary: str # summary = title
    author: str
    author_role: Optional[str]
    published: datetime.datetime
    stars: int
    metadata: Dict[str, str]
    labels: List[str]
    description: str # description = main text
    comments: List[Comment]


class MonorailScraper:
    '''
    Uses Chrome to web scrape Monorail issues.
    '''

    driver: WebDriver

    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def scrape(self, url: str):
        raise NotImplementedError('todo') # todo implement
