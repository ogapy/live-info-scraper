from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class SearchBy(Enum):
    ID = By.ID
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    NAME = By.NAME
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME
    CSS_SELECTOR = By.CSS_SELECTOR


class BrowserManager:
    def __init__(self, start_url):
        self.start_url = start_url
        self.browser = self._activate_browser()

    def _activate_browser(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
        browser.get(self.start_url)
        return browser

    def send_keys(self, by: SearchBy, value: str, keys: str):
        self.find_element(by, value).send_keys(keys)

    def click(self, by: SearchBy, value: str):
        self.find_element(by, value).click()

    def find_element(self, by: SearchBy, value: str):
        return self.browser.find_element(by.value, value)

    def find_elements(self, by: SearchBy, value: str):
        return self.browser.find_elements(by.value, value)

    def get(self, url):
        self.browser.get(url)

    def back(self):
        self.browser.back()

    def close_browser(self):
        self.browser.quit()
