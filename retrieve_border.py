import os
import time
from datetime import datetime

import requests as r
import PySimpleGUI as sg
from pandas import DataFrame, merge

TAR_RANK: list = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    20, 30, 40, 50, 100,
    200, 300, 400, 500, 1000,
    2000, 3000, 4000, 5000, 10000,
    20000, 30000, 40000, 50000, 100000
]
BASE_URL: str = "https://api.sekai.best/event/{event_id}/rankings/graph?rank={rank}"


def get_event_id() -> int:
    while True:
        event_id: str = sg.popup_get_text("Enter the event ID.")
        if event_id.isnumeric():
            return int(event_id)
        sg.popup("Enter the event_id numerically, please.")


def init_dir(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def fmt_the_date(dt_str: str) -> str:
    dt_str = dt_str.replace("T", " ")
    return datetime.fromisoformat(dt_str[:-5])


def main():
    output_dir: str = "./output"
    init_dir(output_dir)
    event_id: int = get_event_id()
    df: DataFrame = DataFrame()
    for rank in TAR_RANK:
        print(f"Get the TOP{rank} border.")
        url: str = BASE_URL.format(event_id=event_id, rank=rank)
        res = r.get(url).json()
        time.sleep(1)
        border_raw_list: list = res["data"]["eventRankings"]
        border_list: list = [
            {"datetime": fmt_the_date(rec["timestamp"]), f"TOP{rank}": rec["score"]}
            for rec in border_raw_list
        ]
        cdf: DataFrame = DataFrame(border_list)
        if df.empty:
            cdf = cdf.sort_values("datetime")
            df = cdf
            continue
        df = merge(df, cdf, on="datetime")
    output_path: str = f"{output_dir}/{event_id:05}_border.csv"
    df.to_csv(output_path, index=False)
    sg.popup(f"The border was output to the following file path.\nPath: {output_path}")


if __name__ == "__main__":
    main()
