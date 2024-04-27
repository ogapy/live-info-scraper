from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Entity.live import Live, Prefecture
from Entity.ticket import Ticket
from scraper import Scraper
from util.date_range import DateRange


class EPlusScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)

    def search_live(self, artist: str):
        browser = self._activate_browser()

        self._move_artist_search_result(browser, artist)
        lives_url = self._scan_lives_url(browser)

        lives = self._scan_lives(lives_url, browser)
        print(lives)

    def _activate_browser(self):
        options = Options()
        browser = webdriver.Chrome(options=options)
        browser.get(self.url)
        return browser

    def _move_artist_search_result(self, browser: webdriver.Chrome, artist: str):
        browser.find_element(By.ID, "head_keyword").send_keys(artist)
        browser.find_element(By.ID, "head_search").click()

    def _scan_lives_url(self, browser: webdriver.Chrome):
        return [
            live.get_attribute("href")
            for live in browser.find_elements(
                By.CSS_SELECTOR,
                "a[href*='/sf/detail/']",
            )
        ]

    def _scan_lives(self, urls: list[str], browser: webdriver.Chrome) -> list[Live]:
        return [self._scan_live(url, browser) for url in urls]

    def _scan_live(self, live_detail_url: str, browser: webdriver.Chrome) -> Live:
        browser.get(live_detail_url)
        tickets: list[Ticket] = [
            Ticket(
                name="チケット",
                apply_status="申込期間",
                apply_period=DateRange(
                    start_date=datetime.fromisoformat("2021-09-01"),
                    end_date=datetime.fromisoformat("2021-09-30"),
                ),
            )
        ]
        live = Live(
            name="ライブ",
            start_date=datetime.fromisoformat("2021-10-01"),
            prefecture=Prefecture.Tokyo,
            venue="東京ドーム",
            website_url=live_detail_url,
            tickets=tickets,
        )
        browser.back()
        return live
