import sys

from pandas import DataFrame, merge

from pkg.utils import BorderAPI, get_event_id, init_dir, popup

TAR_RANK: list = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    20, 30, 40, 50, 100,
    200, 300, 400, 500, 1000,
    2000, 3000, 4000, 5000, 10000,
    20000, 30000, 40000, 50000, 100000
]


def rm_user_data(df: DataFrame) -> DataFrame:
    rm_cols: list = [
        rm_col for rm_col in df.columns.tolist()
        if "UID" in rm_col or "userName" in rm_col
    ]
    for rm_col in rm_cols:
        del df[rm_col]
    return df


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
    # Output
    output_path: str = f"{output_dir}/{event_id:05}_border.csv"
    df = rm_user_data(df)
    df.to_csv(output_path, index=False)
    if not is_exist_args:
        popup(
            "The border was output to the following file path.\n"
            f"Path: {output_path}"
        )


if __name__ == "__main__":
    main()
