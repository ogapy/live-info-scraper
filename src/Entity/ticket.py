from enum import Enum

from pydantic import BaseModel

from util.date_range import DateRange


class TicketApplyState(str, Enum):
    Apply = "受付中"
    SoldOut = "予定枚数終了"
    NotApply = "受付前"
    End = "受付終了"


class Ticket(BaseModel):
    name: str
    apply_status: TicketApplyState
    raw_apply_period: str
    apply_period: DateRange
