import datetime
import time
import datefinder
from typing import List, Dict, Optional, NewType, Iterator

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

import string_util
from issue import Comment, Issue
from string_util import capture

class ScrapeException(Exception):
    pass # todo: add message asking people to report an issue


IssueWebElement = NewType('IssueWebElement', WebElement)
LeftColumnWebElement = NewType('LeftColumnWebElement', WebElement)
RightColumnWebElement = NewType('RightColumnWebElement', WebElement)
HeaderWebElement = NewType('HeaderWebElement', WebElement)
IssueDetailsWebElement = NewType('IssueDetailsWebElement', WebElement)


class IssueScraper:
    """
    Uses Chrome to web scrape Monorail issues.
    """

    driver: WebDriver

    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def scrape(self, issue_url: str) -> Issue:
        """
        :param issue_url: The page of the issue report to scrape from
        :return: the scraped Issue
        """
        project = self._get_project(issue_url)

        issue_elem = self._get_issue_elem(issue_url)

        left_col = self._get_left_column(issue_elem)
        num_stars = self._get_num_stars(left_col)
        metadata = self._get_metadata(left_col)
        labels = self._get_labels(left_col)

        right_col = self._get_right_column(issue_elem)
        header = self._get_header(right_col)
        id = self._get_id(header)
        summary = self._get_summary(header)
        author = self._get_author(header)
        author_roles = self._get_author_roles(header)
        published = self._get_published(header)
        issue_details = self._get_issue_details(right_col)
        description = self._get_description(issue_details)
        comments = self._get_comments(issue_details)

        retrieved = datetime.datetime.now()

        scraped_issue = Issue(retrieved=retrieved, project=project,
                              id=id, summary=summary, author=author, author_roles=author_roles,
                              published=published, stars=num_stars, metadata=metadata, labels=labels,
                              description=description, comments=comments)

        return scraped_issue

    @staticmethod
    def _get_project(issue_url):
        return capture(issue_url, r'/p/(.+)/issues')

    def _get_shadow_root(self, elem: WebElement) -> WebElement:
        # derived from https://www.seleniumeasy.com/selenium-tutorials/accessing-shadow-dom-elements-with-webdriver
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', elem)
        return shadow_root

    @staticmethod
    def _get_datetime(datetime_str: str) -> datetime.datetime:
        matches = list(datefinder.find_dates(datetime_str))
        assert len(matches) == 1
        match = matches[0]
        return match

    def _get_issue_elem(self, url: str) -> IssueWebElement:
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

        return IssueWebElement(issue_elem)

    def _get_left_column(self, issue_elem: IssueWebElement) -> LeftColumnWebElement:
        """
        :param issue_elem: output of self._get_issue_elem
        :return: the (shadow) element that contains the left column, which contains stars, metadata, and labels
        """
        metadata_container = issue_elem.find_element_by_class_name('metadata-container')
        mr_issue_metadata = metadata_container.find_element_by_tag_name('mr-issue-metadata')
        mr_issue_metadata_shadow = self._get_shadow_root(mr_issue_metadata)

        return LeftColumnWebElement(mr_issue_metadata_shadow)

    def _get_num_stars(self, left_column: LeftColumnWebElement) -> int:
        """
        :param left_column: output of self._get_left_column
        :return: number of stars
        """
        star_line_elem = left_column.find_element_by_class_name('star-line')
        star_line_text = star_line_elem.text
        num_stars = int(string_util.capture(star_line_text, r'Starred by ([0-9]+) users?')) # r'users?' matches user or users
        return num_stars

    @staticmethod
    def _get_text_if_possible(web_elem: Optional[WebElement]) -> str:
        """
        :param web_elem: A possibly null WebElement
        :return: Empty string if web_elem is null; web_elem.text otherwise
        """
        if web_elem is None:
            return ''
        else:
            return web_elem.text

    def _get_metadata(self, left_column: LeftColumnWebElement) -> Dict[str, str]:
        """
        :param left_column: output of self._get_left_column
        :return: dict of metadata header -> data (e.g: 'Modified' -> 'Feb 10, 2020')
        """
        mr_metadata = left_column.find_element_by_tag_name('mr-metadata')
        mr_metadata_shadow = self._get_shadow_root(mr_metadata)

        table_rows = mr_metadata_shadow.find_elements_by_tag_name('tr')

        # get rid of cue-availability_msgs
        table_rows = [tr for tr in table_rows if tr.get_attribute('class') != 'cue-availability_msgs']

        table_header_elems: Iterator[Optional[WebElement]] = map(lambda tr: tr.find_element_by_tag_name('th'), table_rows)
        table_data_elems: Iterator[Optional[WebElement]] = map(lambda tr: tr.find_element_by_tag_name('td'), table_rows)

        table_headers: Iterator[str] = map(lambda th: self._get_text_if_possible(th), table_header_elems)
        table_data: Iterator[str] = map(lambda td: self._get_text_if_possible(td), table_data_elems)

        #delete colons from headers
        table_headers = map(lambda header: header.replace(':', ''), table_headers)

        metadata_table = dict(zip(table_headers, table_data))
        return metadata_table

    def _get_labels(self, left_column: LeftColumnWebElement) -> List[str]:
        """
        :param left_column:
        :return:
        """
        labels_container = left_column.find_element_by_class_name('labels-container')
        label_elems = labels_container.find_elements_by_class_name('label')

        labels: Iterator[str] = map(lambda label_elem: label_elem.text, label_elems)
        return list(labels)

    def _get_right_column(self, issue_elem: IssueWebElement) -> RightColumnWebElement:
        container_issue = issue_elem.find_element_by_class_name('container-issue')
        return RightColumnWebElement(container_issue)

    def _get_header(self, right_column: RightColumnWebElement) -> HeaderWebElement:
        issue_header_container = right_column.find_element_by_class_name('issue-header-container')
        mr_issue_header = issue_header_container.find_element_by_tag_name('mr-issue-header')
        mr_issue_header_shadow = self._get_shadow_root(mr_issue_header)
        main_text = mr_issue_header_shadow.find_element_by_class_name('main-text')
        return HeaderWebElement(main_text)

    def _get_id(self, header: HeaderWebElement) -> int:
        header_text = header.text
        return int(capture(header_text, r'Issue ([0-9]+?):'))

    def _get_summary(self, header: HeaderWebElement) -> str:
        header_text = header.text
        return capture(header_text, r'Issue [0-9]+?: (.+?)[\n$]')

    def _get_author(self, header: HeaderWebElement) -> str:
        mr_user_link = header.find_element_by_tag_name('mr-user-link')
        return mr_user_link.text

    def _get_author_roles(self, header: HeaderWebElement) -> List[str]:
        role_label_elems = header.find_elements_by_class_name('role-label')
        role_labels: Iterator[str] = map(lambda elem: elem.text, role_label_elems)
        return list(role_labels)

    def _get_published(self, header: HeaderWebElement) -> datetime.datetime:
        chops_timestamp = header.find_element_by_tag_name('chops-timestamp')
        time_published_str = chops_timestamp.get_attribute('title')
        time_published = self._get_datetime(time_published_str)
        return time_published

    def _get_issue_details(self, right_column: RightColumnWebElement) -> IssueDetailsWebElement:
        container_issue_content = right_column.find_element_by_class_name('container-issue-content')
        mr_issue_details = container_issue_content.find_element_by_tag_name('mr-issue-details')
        mr_issue_details_shadow = self._get_shadow_root(mr_issue_details)
        return IssueDetailsWebElement(mr_issue_details_shadow)

    def _get_description(self, issue_details: IssueDetailsWebElement):
        description_elem = issue_details.find_element_by_tag_name('mr-description')
        return description_elem.text

    def _get_comments(self, issue_details: IssueDetailsWebElement) -> List[Comment]:
        mr_comment_list = issue_details.find_element_by_tag_name('mr-comment-list')
        mr_comment_list_shadow = self._get_shadow_root(mr_comment_list)

        mr_comment_elems = mr_comment_list_shadow.find_elements_by_tag_name('mr-comment')
        comments: Iterator[Comment] = map(lambda elem: self._get_comment(elem), mr_comment_elems)
        return list(comments)

    def _get_comment(self, mr_comment: WebElement) -> Comment:
        mr_comment_shadow = self._get_shadow_root(mr_comment)
        comment_header = mr_comment_shadow.find_element_by_class_name('comment-header')
        div_under_comment_header = comment_header.find_element_by_tag_name('div')

        # fixme: crashes with deleted comments (e.g.: project-zero Issue #1)

        index = self._get_comment_index(div_under_comment_header)
        author = self._get_comment_author(div_under_comment_header)
        role_labels = self._get_comment_author_roles(div_under_comment_header)
        time_published = self._get_comment_published_datetime(div_under_comment_header)
        issue_diff = self._get_comment_issue_diff(mr_comment_shadow)
        comment_body = self._get_comment_body(mr_comment_shadow)

        comment = Comment(index=index, author=author, author_roles=role_labels, published=time_published,
                          issue_diff=issue_diff, body=comment_body)
        return comment

    def _get_comment_index(self, div_under_comment_header: WebElement) -> int:
        comment_link = div_under_comment_header.find_element_by_class_name('comment-link')
        index = int(capture(comment_link.text, r'Comment ([0-9]+)'))
        return index

    def _get_comment_author(self, div_under_comment_header: WebElement) -> str:
        mr_user_link = div_under_comment_header.find_element_by_tag_name('mr-user-link')
        author = mr_user_link.text
        return author

    def _get_comment_author_roles(self, div_under_comment_header: WebElement) -> List[str]:
        role_label_elems: List[WebElement] = div_under_comment_header.find_elements_by_class_name('role-label')
        role_labels = list(map(lambda elem: elem.text, role_label_elems))
        return role_labels

    def _get_comment_published_datetime(self, div_under_comment_header: WebElement) -> datetime.datetime:
        chops_timestamp = div_under_comment_header.find_element_by_tag_name('chops-timestamp')
        time_published_str = chops_timestamp.get_attribute('title')
        time_published = self._get_datetime(time_published_str)
        return time_published

    def _get_comment_issue_diff(self, mr_comment_shadow: WebElement) -> Optional[str]:
        issue_diff_elem_list = mr_comment_shadow.find_elements_by_class_name('issue-diff')
        if len(issue_diff_elem_list) == 0: #there's no issue diff
            issue_diff = None
        elif len(issue_diff_elem_list) == 1: #there's an issue diff
            issue_diff_elem = issue_diff_elem_list[0]
            issue_diff = issue_diff_elem.text
        else:
            raise ScrapeException('More than one issue-diff found in a comment.')

        return issue_diff

    def _get_comment_body(self, mr_comment_shadow: WebElement) -> str:
        comment_body_elem = mr_comment_shadow.find_element_by_class_name('comment-body')
        comment_body = comment_body_elem.text
        return comment_body
