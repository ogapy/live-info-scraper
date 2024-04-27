from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def search_live(self, artist: str):
        pass
