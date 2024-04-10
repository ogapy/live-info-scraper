from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper(ABC):

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def search_live(self, artist: str):
        pass
