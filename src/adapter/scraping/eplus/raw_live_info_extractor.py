import re
from datetime import datetime

from Entity.live import LiveApplyState, Prefecture, RawLiveInfo
from repository.scraping import SearchBy
from util.date_range import DateRange


class RawLiveInfoExtractor:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager

    def extract_live_details(self, index) -> RawLiveInfo:
        nth_child_index = index + 1
        venue_text = self._extract_venue_text(nth_child_index)
        raw_date_range = self._extract_raw_date_range(nth_child_index)

        return RawLiveInfo(
            name=self._extract_name(nth_child_index),
            raw_date_range=raw_date_range,
            date_range=self._parse_date_range(raw_date_range),
            prefecture=self._parse_prefecture(venue_text),
            venue=self._parse_venue(venue_text),
            apply_status=self._extract_apply_status(nth_child_index),
        )

    def _extract_venue_text(self, nth_child_index: int) -> str:
        return self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({nth_child_index}) .ticket-item__venue",
        ).text

    def _extract_raw_date_range(self, nth_child_index: int) -> str:
        return self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({nth_child_index}) .ticket-item__left",
        ).text

    def _extract_name(self, nth_child_index: int) -> str:
        return self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({nth_child_index}) .ticket-item__title",
        ).text

    def _extract_apply_status(self, nth_child_index: int) -> LiveApplyState:
        raw_apply_status = self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f"a[href*='/sf/detail/']:nth-child({nth_child_index}) .ticket-status__item",
        ).text
        return LiveApplyState(raw_apply_status)

    def _parse_date_range(self, raw_date_range: str) -> DateRange:
        def _parse_date(date: str) -> datetime:
            match = re.search(r"(\d{4})/(\d{1,2})/(\d{1,2})", date)
            if not match:
                raise ValueError(
                    f"日付の形式が正しくありません。raw_date_range: {raw_date_range}"
                )
            year, month, day = map(int, match.groups())

            return datetime(year, month, day)

        dates = raw_date_range.split("\n")
        if len(dates) == 1:
            start_date = end_date = _parse_date(dates[0])
            return DateRange(
                start_date=start_date,
                end_date=end_date,
            )
        elif len(dates) == 2:
            return DateRange(
                start_date=_parse_date(dates[0]),
                end_date=_parse_date(dates[1]),
            )
        else:
            raise ValueError(
                f"日付の形式が正しくありません。raw_date_range: {raw_date_range}"
            )

    def _parse_prefecture(self, venue_text: str) -> Prefecture:
        match = re.search(r"\（([^）]+)\）", venue_text)
        return Prefecture(match.group(1)) if match else Prefecture.Unknown

    def _parse_venue(self, venue_text: str):
        result = re.sub(r"\（[^）]*\）", "", venue_text)
        return result.strip()
