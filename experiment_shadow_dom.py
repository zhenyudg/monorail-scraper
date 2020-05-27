from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver


def expand_shadow_root_elem(driver: WebDriver, elem: WebElement) -> WebElement:
    # derived from https://www.seleniumeasy.com/selenium-tutorials/accessing-shadow-dom-elements-with-webdriver
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', elem)
    return shadow_root


if __name__ == '__main__':
    # requirement: chromedriver is in PATH
    driver = webdriver.Chrome()

    driver.get('https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=20000')

    mr_app = driver.find_element_by_tag_name('mr-app')
    mr_app_shadow = expand_shadow_root_elem(driver, mr_app)
    main = mr_app_shadow.find_element_by_tag_name('main')
    mr_issue_page = main.find_element_by_tag_name('mr-issue-page')
    mr_issue_page_shadow = expand_shadow_root_elem(driver, mr_issue_page)
    issue = mr_issue_page_shadow.find_element_by_id('issue')
    print(issue.text)

    driver.close()
