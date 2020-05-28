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


class ScrapeException(Exception):
    pass # todo: add message asking people to report an issue


class IssueScraper:
    """
    Uses Chrome to web scrape Monorail issues.
    """

    driver: WebDriver

    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def scrape(self, url: str) -> Issue:
        """
        :param url: The page of the issue report to scrape from
        :return: the scraped Issue
        """
        raise NotImplementedError('todo') # todo implement

    def _get_shadow_root(self, elem: WebElement) -> WebElement:
        # derived from https://www.seleniumeasy.com/selenium-tutorials/accessing-shadow-dom-elements-with-webdriver
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', elem)
        return shadow_root

    def _get_issue_elem(self, url: str) -> WebElement:
        """
        :param url: the page of the issue report to scrape from
        :return: the element that contains everything between (and excluding) the top white bar
        (the one w/ the search bar) and the bottom row of links (starting w/ "About Monorail")
        """
        self.driver.get(url)

        mr_app = self.driver.find_element_by_tag_name('mr-app')
        mr_app_shadow = self._get_shadow_root(mr_app)
        main = mr_app_shadow.find_element_by_tag_name('main')
        mr_issue_page = main.find_element_by_tag_name('mr-issue-page')
        mr_issue_page_shadow = self._get_shadow_root(mr_issue_page)

        # sometimes (nondeterministically) the issue element is not ready/otherwise missing
        # current solution is to wait a second before retrying, and try at most 5 times
        # there's probably a more clever solution w/ WebDriverWait, but this works for now
        issue_elem: WebElement
        issue_elem_is_found = False
        num_attempts_to_get_issue_elem = 0
        while not issue_elem_is_found:
            try:
                issue_elem = mr_issue_page_shadow.find_element_by_id('issue')
                issue_elem_is_found = True
            except NoSuchElementException:
                time.sleep(1)
                num_attempts_to_get_issue_elem += 1

                if num_attempts_to_get_issue_elem > 5:
                    ScrapeException('Unable to get the issue element.')

        return issue_elem

