from pydantic import BaseModel

from util.date_range import DateRange


class Ticket(BaseModel):
    name: str
    # 申し込みのステータス
    apply_status: str
    # 申し込みの期間
    apply_period: DateRange
