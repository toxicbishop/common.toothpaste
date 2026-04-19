"""
Draw a name onto the GitHub contribution graph for a given year.
Uses the font from name_art.py, maps the 7x52 grid to real dates,
and makes backdated commits so filled cells render as green squares.

Usage:
    python draw_name.py --name toxicbishop --year 2022 --dry-run
    python draw_name.py --name toxicbishop --year 2022 --push
"""

import argparse
import os
import subprocess
import sys
from datetime import date, timedelta

from name_art import render, ROWS, COLS

COMMITS_PER_CELL = 5  # darker square; tune 3-10
DATA_FILE = "data.txt"


def first_sunday_of_year(year: int) -> date:
    d = date(year, 1, 1)
    # weekday(): Mon=0 .. Sun=6. GitHub graph starts columns on Sunday.
    offset = (6 - d.weekday()) % 7
    return d + timedelta(days=offset)


def cells_to_dates(grid, year: int):
    start = first_sunday_of_year(year)
    dates = []
    for col in range(COLS):
        for row in range(ROWS):
            if grid[row][col]:
                day = start + timedelta(days=col * 7 + row)
                if day.year == year:
                    dates.append(day)
    return dates


def make_commit(when: date, idx: int):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{when.isoformat()} #{idx}\n")

    iso = f"{when.isoformat()}T12:00:00"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = iso
    env["GIT_COMMITTER_DATE"] = iso

    subprocess.run(["git", "add", DATA_FILE], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"art: {when.isoformat()} #{idx}"],
        check=True,
        env=env,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Name to draw (a-z, 0-9, space).")
    ap.add_argument("--year", type=int, required=True, help="Target year, e.g. 2022.")
    ap.add_argument("--commits-per-cell", type=int, default=COMMITS_PER_CELL)
    ap.add_argument("--dry-run", action="store_true", help="Preview, make no commits.")
    ap.add_argument("--push", action="store_true", help="git push after committing.")
    args = ap.parse_args()

    try:
        grid = render(args.name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    dates = cells_to_dates(grid, args.year)
    total = len(dates) * args.commits_per_cell

    print(f"Name: {args.name!r}   Year: {args.year}")
    print(f"Filled cells: {len(dates)}   Commits/cell: {args.commits_per_cell}")
    print(f"Total commits to create: {total}")

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
        if i % 10 == 0:
            print(f"  {i}/{len(dates)} cells done")

    print(f"\nDone. {total} commits created.")

    if args.push:
        subprocess.run(["git", "push"], check=True)
        print("Pushed.")
    else:
        print("Not pushed. Run `git push` when ready.")


if __name__ == "__main__":
    main()
