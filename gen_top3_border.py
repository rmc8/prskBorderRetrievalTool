import sys
from dataclasses import dataclass

from pandas import DataFrame, merge

from pkg.utils import BorderAPI, get_event_id, init_dir, popup

TAR_RANK: list = [n for n in range(1, 11)]


@dataclass
class USER:
    def __init__(self, name: str, uid: int):
        self.name: str = name
        self.uid: int = uid


class TOP:
    def __init__(self, last_rec: dict):
        self.t1: USER = USER(
            last_rec["TOP1_userName"],
            last_rec["TOP1_UID"],
        )
        self.t2: USER = USER(
            last_rec["TOP2_userName"],
            last_rec["TOP2_UID"],
        )
        self.t3: USER = USER(
            last_rec["TOP3_userName"],
            last_rec["TOP3_UID"],
        )


def set_target_uid(uid):
    def inner(row):
        for rank in TAR_RANK:
            if uid == row[f"TOP{rank}_UID"]:
                return row[f"TOP{rank}"]
    return inner


def main():
    output_dir: str = "./output"
    init_dir(output_dir)
    args: list = sys.argv
    is_exist_args: bool = len(args) > 1
    event_id: int = int(args[1]) if is_exist_args else get_event_id()
    df: DataFrame = DataFrame()
    for rank in TAR_RANK:
        print(f"Get the TOP{rank} border")
        ba = BorderAPI(event_id=event_id, rank=rank)
        cdf: DataFrame = ba.get_border_df()
        if df.empty:
            cdf = cdf.sort_values("datetime")
            df = cdf
            continue
        df = merge(df, cdf, on="datetime")
    # Create top 3 borders based on user criteria.
    last_rec: dict = df.to_dict(orient="records")[-1]
    top: TOP = TOP(last_rec)
    t1 = set_target_uid(top.t1.uid)
    t2 = set_target_uid(top.t2.uid)
    t3 = set_target_uid(top.t3.uid)
    df[top.t1.name] = df.apply(t1, axis=1)
    df[top.t2.name] = df.apply(t2, axis=1)
    df[top.t3.name] = df.apply(t3, axis=1)
    df = df[["datetime", top.t1.name, top.t2.name, top.t3.name]]

    # Output
    output_path: str = f"{output_dir}/{event_id:05}_top3_border.csv"
    df.to_csv(output_path, index=False)
    if not is_exist_args:
        popup(
            "The border was output to the following file path.\n"
            f"Path: {output_path}"
        )


if __name__ == "__main__":
    main()
