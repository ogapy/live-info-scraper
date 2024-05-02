from datetime import datetime

from Entity.live import Live
from Entity.ticket import Ticket
from repository.scraping.browser_manager import BrowserManager, SearchBy
from repository.scraping.eplus.live_detail_extractor import LiveDetailsExtractor
from scraper import Scraper
from util.date_range import DateRange


class EPlusScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)
        self.browser_manager = BrowserManager(url)
        self.live_details_extractor = LiveDetailsExtractor(self.browser_manager)

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
            self.browser_manager.get_element_attribute(live_link, "href")
            for live_link in self.browser_manager.find_elements(
                SearchBy.CSS_SELECTOR,
                "a[href*='/sf/detail/']",
            )
        ]

    def _scan_lives(self, urls: list[str]):
        return [self._scan_live(url, i) for i, url in enumerate(urls)]

    def _scan_live(self, live_detail_url: str, index: int):
        # ライブの一覧ページにいます
        raw_live_infos = self.live_details_extractor.extract_live_details(index)
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
