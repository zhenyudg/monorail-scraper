import time
from typing import List, Dict, Optional, Tuple

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver


def expand_shadow_root_elem(driver: WebDriver, elem: WebElement) -> WebElement:
    # derived from https://www.seleniumeasy.com/selenium-tutorials/accessing-shadow-dom-elements-with-webdriver
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', elem)
    return shadow_root


# naming convention: WebElement variables are named after their tag/id/class names.
# LIST_${name} is a list of such WebElements.
# ${name}_shadow is the shadow root of the prefix element.
# violations of the naming convention occurs for super-generic elements w/o any specific identifier (e.g: div_under_comment_header)


def scrape_comment(driver: WebDriver, mr_comment: WebElement):
    mr_comment_shadow = expand_shadow_root_elem(driver, mr_comment)
    comment_header = mr_comment_shadow.find_element_by_class_name('comment-header')
    div_under_comment_header = comment_header.find_element_by_tag_name('div')

    # Comment number.
    comment_link = div_under_comment_header.find_element_by_class_name('comment-link')
    # print(comment_link.text) # todo capture comment number from comment_link.text with r'Comment ([0-9]+)'

    # User who posted comment.
    mr_user_link = div_under_comment_header.find_element_by_tag_name('mr-user-link')
    # print(mr_user_link.text)

    # Timestamp of comment.
    chops_timestamp = div_under_comment_header.find_element_by_tag_name('chops-timestamp')
    post_time: str = chops_timestamp.get_attribute('title') # todo: make a helper function to deduplicate this attribute query for chops-timestamp elems
    # print(post_time)

    # Role(s) of the user.
    LIST_role_label = div_under_comment_header.find_elements_by_class_name('role-label')
    # print(*[role_label.text for role_label in LIST_role_label])


def get_text_if_possible(web_elem: Optional[WebElement]) -> Optional[str]:
    if web_elem is None:
        return None
    else:
        return web_elem.text


def scrape_metadata(mr_metadata_shadow: WebElement):
    LIST_tr = mr_metadata_shadow.find_elements_by_tag_name('tr')

    # get rid of cue-availability_msgs
    LIST_tr = [tr for tr in LIST_tr if tr.get_attribute('class') != 'cue-availability_msgs']

    LIST_th_td: List[Tuple[Optional[WebElement], Optional[WebElement]]] \
        = map(lambda tr: (tr.find_element_by_tag_name('th'), tr.find_element_by_tag_name('td')), LIST_tr)

    metadata_rows: List[Tuple[Optional[str], Optional[str]]] \
        = map(lambda PAIR_th_td: (get_text_if_possible(PAIR_th_td[0]), get_text_if_possible(PAIR_th_td[1])), LIST_th_td)

    # for row in metadata_rows: print(*row)


def scrape_labels(mr_issue_metadata_shadow: WebElement):
    labels_container = mr_issue_metadata_shadow.find_element_by_class_name('labels-container')
    LIST_label = labels_container.find_elements_by_class_name('label')

    labels: List[str] = map(lambda label_elem: label_elem.text, LIST_label)
    # print(*labels)


if __name__ == '__main__':
    # requirement: chromedriver is in PATH
    driver = webdriver.Chrome()

    driver.get('https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000')

    mr_app = driver.find_element_by_tag_name('mr-app')
    mr_app_shadow = expand_shadow_root_elem(driver, mr_app)
    main = mr_app_shadow.find_element_by_tag_name('main')
    mr_issue_page = main.find_element_by_tag_name('mr-issue-page')
    mr_issue_page_shadow = expand_shadow_root_elem(driver, mr_issue_page)

    # issue is everything between (and excluding) the top white bar (the one w/ the search bar)
    # and the bottom row of links (starting w/ "About Monorail")
    # sometimes (nondeterministically) the issue element is not ready/otherwise missing
    # current solution is to wait a second before retrying, and try at most 5 times
    # there's probably a more clever solution w/ WebDriverWait, but this works for now
    issue_elem_is_found = False
    num_attempts_to_get_issue_elem = 0
    while not issue_elem_is_found and num_attempts_to_get_issue_elem < 5:
        try:
            issue = mr_issue_page_shadow.find_element_by_id('issue')
            issue_elem_is_found = True
        except NoSuchElementException:
            time.sleep(1)
            num_attempts_to_get_issue_elem += 1
    # print(issue.text)

    # left column containing metadata/tags/...
    metadata_container = issue.find_element_by_class_name('metadata-container')
    mr_issue_metadata = metadata_container.find_element_by_tag_name('mr-issue-metadata')
    mr_issue_metadata_shadow = expand_shadow_root_elem(driver, mr_issue_metadata)
    assert mr_issue_metadata_shadow is not None

    star_line = mr_issue_metadata_shadow.find_element_by_class_name('star-line')
    # print(star_line.text) # todo: parse # of stars with r'Starred by ([0-9]+) users?' (maybe)

    # central block of metadata in left column: Owner -> Type
    mr_metadata = mr_issue_metadata_shadow.find_element_by_tag_name('mr-metadata')
    mr_metadata_shadow = expand_shadow_root_elem(driver, mr_metadata)
    scrape_metadata(mr_metadata_shadow)

    scrape_labels(mr_issue_metadata_shadow)

    # right column containing the issue title, main text and comments
    container_issue = issue.find_element_by_class_name('container-issue')

    # grey header containing the issue title, reporter, and report date
    issue_header_container = container_issue.find_element_by_class_name('issue-header-container')
    # print(issue_header_container.text)

    # main text and comments
    container_issue_content = container_issue.find_element_by_class_name('container-issue-content')
    mr_issue_details = container_issue_content.find_element_by_tag_name('mr-issue-details')
    mr_issue_details_shadow = expand_shadow_root_elem(driver, mr_issue_details)

    # main text
    mr_description = mr_issue_details_shadow.find_element_by_tag_name('mr-description')
    # print(mr_description.text) # good enough to send to oss-fuzz issue parser

    # comments
    mr_comment_list = mr_issue_details_shadow.find_element_by_tag_name('mr-comment-list')
    mr_comment_list_shadow = expand_shadow_root_elem(driver, mr_comment_list)

    LIST_mr_comment = mr_comment_list_shadow.find_elements_by_tag_name('mr-comment')
    for mr_comment in LIST_mr_comment: scrape_comment(driver, mr_comment)

    driver.close()
