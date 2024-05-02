from datetime import datetime

from pydantic import BaseModel


class DateRangeError(ValueError):
    """日付範囲が無効であることを示すカスタムエラー"""

    pass


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    def __init__(self, start_date: datetime, end_date: datetime):
        super().__init__(start_date=start_date, end_date=end_date)

        if start_date > end_date:
            raise DateRangeError("開始日は終了日よりも前でなければなりません。")
        self.start_date = start_date
        self.end_date = end_date

    def contains(self, date: datetime) -> bool:
        """指定された日付がこの期間内にあるかどうかを確認します。"""
        return self.start_date <= date <= self.end_date
