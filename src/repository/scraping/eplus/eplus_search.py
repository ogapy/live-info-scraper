import re
from datetime import datetime

from Entity.live import Live, Prefecture, RawLiveInfo
from Entity.ticket import Ticket
from repository.scraping.browser_manager import BrowserManager, SearchBy
from scraper import Scraper
from util.date_range import DateRange


class EPlusScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)
        self.browser_manager = BrowserManager(url)

    def search_live(self, artist: str):
        self._move_artist_search_result(artist)
        lives_url = self._scan_lives_url()

        lives = self._scan_lives(lives_url)
        print(lives)

    def _move_artist_search_result(self, artist: str):
        self.browser_manager.send_keys(SearchBy.ID, "head_keyword", artist)
        self.browser_manager.click(SearchBy.ID, "head_search")

    def _scan_lives_url(self):
        return [
            self.browser_manager.get_attribute(live_link, "href")
            for live_link in self.browser_manager.find_elements(
                SearchBy.CSS_SELECTOR,
                "a[href*='/sf/detail/']",
            )
        ]

    def _scan_lives(self, urls: list[str]):
        return [self._scan_live(url, i) for i, url in enumerate(urls)]

    def _scan_live(self, live_detail_url: str, index: int):
        # ライブの一覧ページにいます
        raw_live_infos = self._scan_live_details(index + 1)
        # tickets = self._scan_tickets_details(live_detail_url, browser)

        self.browser_manager.get(live_detail_url)
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
        self.browser_manager.back()
        return live

    def _scan_live_details(self, index: int):
        venue_text = self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({index}) .ticket-item__venue",
        ).text
        raw_date_range = self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({index}) .ticket-item__left",
        ).text
        start_date, end_date = self._extract_date_range(raw_date_range)

        return RawLiveInfo(
            name=self.browser_manager.find_element(
                SearchBy.CSS_SELECTOR,
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
