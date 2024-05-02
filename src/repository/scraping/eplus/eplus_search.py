from datetime import datetime

from Entity.live import Live
from Entity.ticket import Ticket
from scraper import Scraper
from util.date_range import DateRange

from repository.scraping.browser_manager import BrowserManager, SearchBy
from repository.scraping.eplus.live_detail_extractor import LiveDetailsExtractor


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
        raw_live_infos = self.live_details_extractor.extract_live_details(index)

        self.browser_manager.get(live_detail_url)
        tickets = self._scan_tickets_details(live_detail_url)
        live = self._create_live_object(raw_live_infos, live_detail_url, tickets)
        self.browser_manager.back()
        return live

    def _scan_tickets_details(self) -> list[Ticket]:
        return [
            Ticket(
                name="チケット",
                apply_status="申込期間",
                apply_period=DateRange(
                    start_date=datetime(2021, 9, 1),
                    end_date=datetime(2021, 9, 30),
                ),
            )
        ]

    def _create_live_object(self, raw_live_infos, live_detail_url, tickets) -> Live:
        return Live(
            name=raw_live_infos.name,
            raw_date_range=raw_live_infos.raw_date_range,
            date_range=raw_live_infos.date_range,
            prefecture=raw_live_infos.prefecture,
            venue=raw_live_infos.venue,
            website_url=live_detail_url,
            tickets=tickets,
        )
