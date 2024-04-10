from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Entity.live import Live
from src.repository.scraping.scraper import Scraper


class EPlusScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)

    def search_live(self, artist: str):
        browser = self._activate_browser()

        self._move_artist_search_result(browser, artist)
        lives_url = self._scan_lives(browser)

        apply_ranges = []
        for url in lives_url:
            browser.get(url)
            apply_range = browser.find_element(
                By.CSS_SELECTOR,
                "section.block-ticket:not(.hidden) p.block-ticket__time",
            ).text
            apply_ranges.append(apply_range)
            browser.back()
        print(apply_ranges)

    def _activate_browser(self):
        options = Options()
        browser = webdriver.Chrome(options=options)
        browser.get(self.url)
        return browser

    def _move_artist_search_result(self, browser: webdriver.Chrome, artist: str):
        browser.find_element(By.ID, "head_keyword").send_keys(artist)
        browser.find_element(By.ID, "head_search").click()

    def _move(self, browser: webdriver.Chrome, url: str):
        browser.get(url)

    def _back(self, browser: webdriver.Chrome):
        browser.back()

    def _scan_lives(self, browser: webdriver.Chrome):
        return [
            live.get_attribute("href")
            for live in browser.find_elements(
                By.CSS_SELECTOR,
                "a[href*='/sf/detail/']",
            )
        ]

    class LiveDetailScanner:
        def __init__(self):
            pass

        def scan(self, urls: list[str], browser: webdriver.Chrome) -> list[Live]:
            return [self._scan_live(url, browser) for url in urls]

        def _scan_live(self, live_detail_url: str, browser: webdriver.Chrome) -> Live:
            self._move(browser, live_detail_url)
            # apply_range = browser.find_element(
            #     By.CSS_SELECTOR,
            #     "section.block-ticket:not(.hidden) p.block-ticket__time",
            # ).text
            # apply_range.append(apply_range)
            self._back(browser)
