"""
Draw a Christmas tree on the GitHub contribution graph in December
of a chosen year. Commits only land on dates in December.

Usage:
    python christmas_tree.py --year 2023 --dry-run
    python christmas_tree.py --year 2023 --push
"""

import argparse
import os
import subprocess
import sys
from datetime import date, timedelta

# 7 rows (Sun..Sat on GitHub) x 5 cols (weeks)
# Row 0 = Sunday, Row 6 = Saturday
TREE = [
    "..X..",  # R0 top
    ".XXX.",  # R1
    "XXXXX",  # R2
    ".XXX.",  # R3
    "XXXXX",  # R4
    "..X..",  # R5 trunk
    "..X..",  # R6 trunk
]

ROWS = 7
COLS = 5
DATA_FILE = "data.txt"
COMMITS_PER_CELL = 6


def row_sun_index(d: date) -> int:
    # Python weekday(): Mon=0..Sun=6. GitHub rows: Sun=0..Sat=6.
    return (d.weekday() + 1) % 7


def col_zero_start(year: int) -> date:
    jan1 = date(year, 1, 1)
    return jan1 - timedelta(days=row_sun_index(jan1))


def column_of(d: date, start: date) -> int:
    return (d - start).days // 7


def december_columns(year: int):
    start = col_zero_start(year)
    dec1 = date(year, 12, 1)
    dec31 = date(year, 12, 31)
    return column_of(dec1, start), column_of(dec31, start), start


def align_tree_columns(year: int):
    """Pick the column offset that puts the most filled cells inside December."""
    first_col, last_col, start = december_columns(year)
    best_col, best_score = first_col, -1
    for base_col in range(first_col - 1, last_col + 2):
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                if TREE[r][c] != "X":
                    continue
                day = start + timedelta(days=(base_col + c) * 7 + r)
                if day.month == 12 and day.year == year:
                    score += 1
        if score > best_score:
            best_score = score
            best_col = base_col
    return best_col


def tree_dates(year: int):
    start = col_zero_start(year)
    base_col = align_tree_columns(year)
    dates = []
    for r in range(ROWS):
        for c in range(COLS):
            if TREE[r][c] == "X":
                day = start + timedelta(days=(base_col + c) * 7 + r)
                if day.month == 12 and day.year == year:
                    dates.append(day)
    return dates


def preview(year: int):
    start = col_zero_start(year)
    base_col = align_tree_columns(year)
    print(f"\nPreview for December {year} (. = skip, # = filled, - = outside Dec):\n")
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            day = start + timedelta(days=(base_col + c) * 7 + r)
            if TREE[r][c] == "X":
                if day.month == 12 and day.year == year:
                    row.append("#")
                else:
                    row.append("-")
            else:
                row.append(".")
        print(" ".join(row))
    print()


def make_commit(when: date, idx: int):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{when.isoformat()} xmas #{idx}\n")

    iso = f"{when.isoformat()}T12:00:00"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = iso
    env["GIT_COMMITTER_DATE"] = iso

    subprocess.run(["git", "add", DATA_FILE], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"xmas: {when.isoformat()} #{idx}"],
        check=True,
        env=env,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, help="Target year, e.g. 2023.")
    ap.add_argument("--commits-per-cell", type=int, default=COMMITS_PER_CELL)
    ap.add_argument("--dry-run", action="store_true", help="Preview only, no commits.")
    ap.add_argument("--push", action="store_true", help="git push after committing.")
    args = ap.parse_args()

    year = args.year
    if year is None:
        try:
            year = int(input("Year? ").strip())
        except ValueError:
            print("Invalid year.", file=sys.stderr)
            sys.exit(1)

    preview(year)
    dates = tree_dates(year)
    total = len(dates) * args.commits_per_cell
    print(f"Filled cells in Dec {year}: {len(dates)}")
    print(f"Commits/cell: {args.commits_per_cell}   Total commits: {total}")

    if args.dry_run:
        print("\nDry run — no commits made.")
        return

    confirm = input(f"\nProceed with {total} real commits? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    for i, day in enumerate(dates, start=1):
        for k in range(args.commits_per_cell):
            make_commit(day, k)
        print(f"  {i}/{len(dates)}: {day.isoformat()}")

    print(f"\nDone. {total} commits created.")

    if args.push:
        subprocess.run(["git", "push"], check=True)
        print("Pushed.")
    else:
        print("Not pushed. Run `git push` when ready.")


if __name__ == "__main__":
    main()
