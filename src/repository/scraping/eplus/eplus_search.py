import re
from datetime import datetime

from Entity.live import Live, Prefecture, RawLiveInfo
from Entity.ticket import Ticket
from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        options.add_argument("--headless")
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

    def _scan_lives(self, urls: list[str], browser: webdriver.Chrome):
        return [self._scan_live(url, browser, i) for i, url in enumerate(urls)]

    def _scan_live(self, live_detail_url: str, browser: webdriver.Chrome, index: int):
        # ライブの一覧ページにいます
        raw_live_infos = self._scan_live_details(browser, index + 1)
        # tickets = self._scan_tickets_details(live_detail_url, browser)

        browser.get(live_detail_url)
        tickets: list[Ticket] = [
            Ticket(
                name="チケット",
                apply_status="申込期間",
                apply_period=DateRange(
                    start_date=datetime(2021, 9, 1),
                    end_date=datetime(2021, 9, 30),
                ),
            )
        ]
        live = Live(
            name=raw_live_infos.name,
            raw_date_range=raw_live_infos.raw_date_range,
            date_range=raw_live_infos.date_range,
            prefecture=raw_live_infos.prefecture,
            venue=raw_live_infos.venue,
            website_url=live_detail_url,
            tickets=tickets,
        )
        browser.back()
        return live

    def _scan_live_details(self, browser: webdriver.Chrome, index: int):
        venue_text = browser.find_element(
            By.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({index}) .ticket-item__venue",
        ).text
        raw_date_range = browser.find_element(
            By.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({index}) .ticket-item__left",
        ).text
        start_date, end_date = self._extract_date_range(raw_date_range)

        return RawLiveInfo(
            name=browser.find_element(
                By.CSS_SELECTOR,
                f"a[href*='/sf/detail/']:nth-child({index}) .ticket-item__title",
            ).text,
            raw_date_range=raw_date_range,
            date_range=DateRange(
                start_date=start_date,
                end_date=end_date,
            ),
            prefecture=Prefecture(self._extract_prefecture(venue_text))
            if self._extract_prefecture(venue_text)
            else Prefecture.Unknown,
            venue=self._extract_venue(venue_text),
        )

    def _extract_date_range(self, raw_date_range: str):
        dates = raw_date_range.split("\n")
        if len(dates) == 1:
            start_date = end_date = self._parse_date(dates[0])
        elif len(dates) == 2:
            start_date = self._parse_date(dates[0])
            end_date = self._parse_date(dates[1])
        else:
            raise ValueError("日付の形式が正しくありません。")

        return start_date, end_date

    def _parse_date(self, date_str):
        year, month, day = map(
            int, re.search(r"(\d{4})/(\d{1,2})/(\d{1,2})", date_str).groups()
        )
        return datetime(year, month, day)

    def _extract_prefecture(self, venue_text: str):
        match = re.search(r"\（([^）]+)\）", venue_text)
        return match.group(1) if match else None

    def _extract_venue(self, venue_text: str):
        result = re.sub(r"\（[^）]*\）", "", venue_text)
        return result.strip()
