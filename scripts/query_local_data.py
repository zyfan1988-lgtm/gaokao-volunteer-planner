import argparse
from pathlib import Path

import pandas as pd


def configure_stdout() -> None:
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    return pd.read_csv(path, encoding="utf-8-sig")


def score_rank(data_root: Path, score: int | None, rank: int | None) -> None:
    table = read_csv(data_root / "yifenyiduan_standard" / "sd_2026_culture_score_rank.csv")
    required = {"score", "all_cumulative"}
    if not required.issubset(table.columns):
        raise ValueError("Score-rank table must include score and all_cumulative.")
    if score is not None:
        hit = table[table["score"] == score]
        print(hit.to_string(index=False) if not hit.empty else f"No exact score row found for {score}.")
    if rank is not None:
        table = table.assign(distance=(table["all_cumulative"] - rank).abs())
        print(table.sort_values(["distance", "score"], ascending=[True, False]).head(8).to_string(index=False))


def actual_admission(data_root: Path, keyword: str | None, rank: int | None, limit: int) -> None:
    table = read_csv(data_root / "sdzk_2026_actual_results" / "sd_2026_regular_batch_admission_normalized.csv")
    aliases = {
        "school": "college_name",
        "major_or_group": "major_name",
        "rank": "minimum_rank",
    }
    for canonical, source in aliases.items():
        if canonical not in table.columns and source in table.columns:
            table[canonical] = table[source]
    required = {"school", "major_or_group", "rank", "round"}
    if not required.issubset(table.columns):
        raise ValueError("Admission table must include school, major_or_group, rank and round.")
    if keyword:
        match = table["school"].fillna("").str.contains(keyword, case=False, regex=False) | table["major_or_group"].fillna("").str.contains(keyword, case=False, regex=False)
        table = table[match]
    if rank is not None:
        table = table.assign(distance=(pd.to_numeric(table["rank"], errors="coerce") - rank).abs())
        table = table.sort_values("distance")
    print(table.head(limit).to_string(index=False))


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Query locally imported, standardized gaokao data.")
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--province")
    parser.add_argument("--year")
    parser.add_argument("--score", type=int)
    parser.add_argument("--rank", type=int)
    parser.add_argument("--actual-keyword")
    parser.add_argument("--actual-rank", type=int)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.score is not None or args.rank is not None:
        score_rank(args.data_root, args.score, args.rank)
    if args.actual_keyword or args.actual_rank is not None:
        actual_admission(args.data_root, args.actual_keyword, args.actual_rank, args.limit)
    if all(value is None for value in [args.score, args.rank, args.actual_keyword, args.actual_rank]):
        parser.error("Provide score/rank or actual-keyword/actual-rank.")


if __name__ == "__main__":
    main()
