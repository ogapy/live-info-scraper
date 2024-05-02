from repository.scraping.eplus.eplus_search import EPlusScraper


def main():
    scraper = EPlusScraper("https://eplus.jp/")
    scraper.search_live("SPITZ")


if __name__ == "__main__":
    main()
