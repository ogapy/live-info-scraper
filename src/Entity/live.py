from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from Entity.ticket import Ticket


# 都道府県のEnum
class Prefecture(str, Enum):
    Hokkaido = "北海道"
    Aomori = "青森"
    Iwate = "岩手"
    Miyagi = "宮城"
    Akita = "秋田"
    Yamagata = "山形"
    Fukushima = "福島"
    Ibaraki = "茨城"
    Tochigi = "栃木"
    Gunma = "群馬"
    Saitama = "埼玉"
    Chiba = "千葉"
    Tokyo = "東京"
    Kanagawa = "神奈川"
    Niigata = "新潟"
    Toyama = "富山"
    Ishikawa = "石川"
    Fukui = "福井"
    Yamanashi = "山梨"
    Nagano = "長野"
    Gifu = "岐阜"
    Shizuoka = "静岡"
    Aichi = "愛知"
    Mie = "三重"
    Shiga = "滋賀"
    Kyoto = "京都"
    Osaka = "大阪"
    Hyogo = "兵庫"
    Nara = "奈良"
    Wakayama = "和歌山"
    Tottori = "鳥取"
    Shimane = "島根"
    Okayama = "岡山"
    Hiroshima = "広島"
    Yamaguchi = "山口"
    Tokushima = "徳島"
    Kagawa = "香川"
    Ehime = "愛媛"
    Kochi = "高知"
    Fukuoka = "福岡"
    Saga = "佐賀"
    Nagasaki = "長崎"
    Kumamoto = "熊本"
    Oita = "大分"
    Miyazaki = "宮崎"
    Kagoshima = "鹿児島"
    Okinawa = "沖縄"


class Live(BaseModel):
    name: str
    start_date: datetime
    prefecture: Prefecture
    venue: str
    website_url: str
    tickets: list[Ticket]
