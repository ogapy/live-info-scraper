from adapter.scraping import BrowserManager, SearchBy
from adapter.scraping.scraper import Scraper
from Entity.live import Live

from .raw_live_info_extractor import RawLiveInfoExtractor
from .ticket_info_extractor import TicketsInfoExtractor


class EPlusScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)
        self.browser_manager = BrowserManager(url)
        self.raw_live_info_extractor = RawLiveInfoExtractor(self.browser_manager)
        self.tickets_info_extractor = TicketsInfoExtractor(self.browser_manager)

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

    def _scan_live(self, live_url: str, index: int):
        raw_live_infos = self.raw_live_info_extractor.extract_live_details(index)

        tickets = self.tickets_info_extractor.extract_tickets(live_url)
        live = self._create_live_object(raw_live_infos, live_url, tickets)
        return live

    def _create_live_object(self, raw_live_infos, live_url, tickets) -> Live:
        return Live(
            name=raw_live_infos.name,
            raw_date_range=raw_live_infos.raw_date_range,
            date_range=raw_live_infos.date_range,
            prefecture=raw_live_infos.prefecture,
            venue=raw_live_infos.venue,
            apply_status=raw_live_infos.apply_status,
            website_url=live_url,
            tickets=tickets,
        )
