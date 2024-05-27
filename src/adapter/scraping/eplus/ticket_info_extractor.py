from datetime import datetime

from adapter.scraping import BrowserManager, SearchBy
from Entity.ticket import Ticket, TicketApplyState
from util.date_range import DateRange
from util.errors import ExtractDateError


class TicketsInfoExtractor:
    def __init__(self, browser_manager: BrowserManager):
        self.browser_manager = browser_manager
        self.ticket_info_extractor = TicketInfoExtractor(browser_manager)

    def extract_tickets(self, live_url) -> list[Ticket]:
        self.browser_manager.get(live_url)

        self._display_closed_apply_tickets()

        ticket_num = self._count_tickets()
        tickets = [
            self.ticket_info_extractor.extract_ticket_details(i)
            for i in range(ticket_num)
        ]

        self.browser_manager.back()

        return tickets

    # 受付は全て終了しました
    def _display_closed_apply_tickets(self):
        self.browser_manager.click(
            SearchBy.CSS_SELECTOR,
            ".block-ticket-0:not(.hidden) a:contains('受付は全て終了しました')",
        )

    def _count_tickets(self) -> int:
        return len(
            self.browser_manager.find_elements(
                SearchBy.CSS_SELECTOR,
                ".block-ticket:not(.hidden)",
            )
        )


class TicketInfoExtractor:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager

    def extract_ticket_details(self, index) -> Ticket:
        nth_child_index = index + 1
        raw_apply_period = self._extract_raw_apply_period(nth_child_index)

        try:
            ticket = Ticket(
                name=self._extract_name(nth_child_index),
                apply_status=self._extract_apply_status(nth_child_index),
                raw_apply_period=raw_apply_period,
                apply_period=self._parse_apply_period(raw_apply_period),
            )
            return ticket
        except ExtractDateError:
            None

    def _extract_name(self, nth_child_index: int) -> str:
        return self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f".block-ticket:nth-child({nth_child_index}) .block-ticket__title",
        ).text

    def _extract_apply_status(self, nth_child_index: int) -> TicketApplyState:
        raw_apply_status = self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f".block-ticket:nth-child({nth_child_index}) .block-ticket__status",
        ).text
        return (
            TicketApplyState(raw_apply_status)
            if raw_apply_status
            else TicketApplyState.End
        )

    def _extract_raw_apply_period(self, nth_child_index: int) -> str:
        raw_apply_period_text = self.browser_manager.find_element(
            SearchBy.CSS_SELECTOR,
            f".block-ticket:nth-child({nth_child_index}) .block-ticket__time",
        ).text
        return raw_apply_period_text.replace("受付期間:", "")

    def _parse_apply_period(self, raw_apply_period: str) -> DateRange:
        split_apply_period = raw_apply_period.split("～")
        try:
            data_range = DateRange(
                start_date=self.convert_to_datetime(split_apply_period[0]),
                end_date=self.convert_to_datetime(split_apply_period[1]),
            )
        except ExtractDateError as e:
            raise e
        return data_range

    def convert_to_datetime(self, date_str):
        # yy/mm/dd(aa)HH:MM の形式
        print(date_str)
        try:
            date, time = date_str.split(")")
            date_parts = date.split("(")
            year, month, day = map(int, date_parts[0].split("/"))
            hour, minute = map(int, time.split(":"))
        except ValueError:
            raise ExtractDateError(f"Invalid date format: {date_str}")

        return datetime(year, month, day, hour, minute)
        return datetime(year, month, day, hour, minute)
