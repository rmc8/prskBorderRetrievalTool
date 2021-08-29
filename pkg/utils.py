import os
import time
from typing import Optional
from datetime import datetime, timedelta

import requests as r
import PySimpleGUI as sg
from pandas import DataFrame


def get_event_id() -> int:
    while True:
        event_id: Optional[str] = sg.popup_get_text("Enter the event ID.")
        if event_id is None:
            exit()
        elif event_id.isnumeric():
            return int(event_id)
        sg.popup("Enter the event_id numerically, please.")


def init_dir(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def popup(msg: str):
    sg.popup(msg)


class BorderAPI:
    def __init__(self, event_id: int, rank: int):
        BASE_URL: str = "https://api.sekai.best/event/{event_id}/rankings/graph?rank={rank}"
        self.rank: int = rank
        self.url: str = BASE_URL.format(event_id=event_id, rank=rank)

    @staticmethod
    def fmt_the_date(dt_str: str) -> datetime:
        dt_str = dt_str.replace("T", " ")
        return datetime.fromisoformat(dt_str[:-5]) + timedelta(hours=9)

    def get_border_df(self) -> DataFrame:
        res = r.get(self.url).json()
        time.sleep(1)
        border_raw_list: list = res["data"]["eventRankings"]
        border_list: list = [
            {
                "datetime": self.fmt_the_date(rec["timestamp"]),
                f"TOP{self.rank}": rec["score"],
                f"TOP{self.rank}_UID": rec["userId"],
                f"TOP{self.rank}_userName": rec["userName"],
            }
            for rec in border_raw_list
        ]
        cdf: DataFrame = DataFrame(border_list)
        return cdf
