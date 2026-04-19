import os
import sys
import random
import subprocess
import time
import argparse
from datetime import datetime, timedelta, timezone

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_year_offset(prompt, default=-1):
    """
    Asks user for a year offset. 
    0 = Current Year
    -1 = Previous Year
    -2 = Two Years Ago, etc.
    """
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            # Check if input is a valid integer (handles negative signs)
            value = int(user_input)
            if value > 0:
                 print("Please enter 0 or a negative integer (e.g., -1 for last year).")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer (e.g., -1, -2).")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def get_git_config(config_name, cwd="."):
    try:
        result = subprocess.run(["git", "config", config_name], 
                                cwd=cwd, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return None

def random_date_in_year(year_offset):
    """
    Generates a random date within the specific target year.
    Uses system local time but ensures it's compatible with Git's requirements.
    """
    now = datetime.now()
    target_year = now.year + year_offset
    
    # Start of the target year
    start_date = datetime(target_year, 1, 1)
    
    if target_year == now.year:
        end_date = now
    else:
        end_date = datetime(target_year, 12, 31, 23, 59, 59)
    
    time_between_dates = end_date - start_date
    if time_between_dates.total_seconds() <= 0:
        return start_date

    random_seconds = random.randint(0, int(time_between_dates.total_seconds()))
    commit_date = start_date + timedelta(seconds=random_seconds)
    
    return commit_date

def make_commit(date, repo_path, filename, message="🌱 graph-greener: filling squares!"):
    filepath = os.path.join(repo_path, filename)
    
    # Append timestamp to the file
    try:
        with open(filepath, "a") as f:
            f.write(f"Commit at {date.isoformat()}\n")
    except IOError as e:
        print(f"❌ Error writing to file {filepath}: {e}")
        return False

    # Prep the date for Git (ISO 8601 with local timezone is best)
    # Using local timezone info if possible
    local_tz = datetime.now().astimezone().tzinfo
    date_with_tz = date.replace(tzinfo=local_tz)
    date_str = date_with_tz.isoformat()

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Fast add
    subprocess.run(["git", "add", filename], cwd=repo_path, capture_output=True)
    
    # Commit
    res = subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env, capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"❌ Git commit failed: {res.stderr.strip()}")
        return False
    return True

def get_date_from_grid(year, col, row):
    """
    Maps a grid coordinate (col: week 0-52, row: day 0-6) to a datetime.
    Row 0 is Sunday, Row 6 is Saturday.
    """
    # Start with Jan 1st of the year
    first_day_of_year = datetime(year, 1, 1)
    # Find the nearest preceding Sunday (the start of the grid)
    # weekday(): Mon=0, Sun=6. GitHub row 0 is Sunday.
    # If Jan 1st is Monday (0), offset is 1. If Sunday (6), offset is 0.
    start_offset = (first_day_of_year.weekday() + 1) % 7
    grid_start = first_day_of_year - timedelta(days=start_offset)
    
    target_date = grid_start + timedelta(weeks=col, days=row)
    
    # Ensure it's not in the future or outside the year if we care
    if target_date.year != year and col < 2: # handle wrap around
         pass
    return target_date

PATTERNS = {
    "pacman": [
        "  #####  ",
        " ####### ",
        "##  #####",
        "######## ",
        "##  #####",
        " ####### ",
        "  #####  "
    ],
    "heart": [
        "  ##   ##  ",
        " #### #### ",
        "###########",
        "###########",
        " ######### ",
        "  #######  ",
        "    ###    "
    ],
    "blocks": [
        "########",
        "########",
        "########",
        "########",
        "########",
        "########",
        "########"
    ]
}

def main():
    parser = argparse.ArgumentParser(description="🌱 graph-greener: The Premium GitHub Graph Generator")
    parser.add_argument("--commits", type=int, help="Number of total commits")
    parser.add_argument("--offset", type=int, help="Year offset (e.g. -1 for last year)")
    parser.add_argument("--repo", type=str, help="Path to git repository")
    parser.add_argument("--file", type=str, default="data.txt", help="Filename to modify")
    parser.add_argument("--push", action="store_true", help="Automatically push after commits")
    parser.add_argument("--silent", action="store_true", help="Bypass interactive prompts")
    parser.add_argument("--pattern", type=str, choices=["pacman", "heart", "blocks"], help="Pattern to draw")
    
    args = parser.parse_args()

    # Premium UI Header
    if not args.silent:
        print("\033[1;32m" + "="*60 + "\033[0m")
        print("\033[1;32m🌱 graph-greener - The Premium GitHub Graph Generator 🌱\033[0m")
        print("\033[1;32m" + "="*60 + "\033[0m")
        print("Populate your contribution graph with elegant green activity.\n")

    # Initial inputs
    if args.silent:
        num_commits = args.commits if args.commits else 20
        year_offset = args.offset if args.offset is not None else 0
        repo_path = args.repo if args.repo else "."
        filename = args.file
    else:
        # Identity Check
        git_email = get_git_config("user.email")
        if not git_email:
            print("\033[1;31m⚠️  WARNING:\033[0m No Git email configured globally.")
        else:
            print(f"👤 Committing as: \033[1;36m{git_email}\033[0m\n")

        num_commits = args.commits if args.commits else get_positive_int("How many total commits would you like", 20)
        
        current_year = datetime.now().year
        if args.offset is not None:
            year_offset = args.offset
        else:
            print(f"Select target year (0 for {current_year}, -1 for {current_year-1})")
            year_offset = get_year_offset("Year Offset", -1)
        
        repo_path = args.repo if args.repo else get_repo_path("Repository Path", ".")
        filename = args.file if args.file != "data.txt" else get_filename("Filename to modify", "data.txt")

    # Validation
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"\033[1;31m❌ ERROR:\033[0m {repo_path} is not a Git repository.")
        sys.exit(1)

    target_year_display = datetime.now().year + year_offset
    if not args.silent:
        print(f"\n🚀 \033[1;32mStarting batch process...\033[0m")
        print(f"Year: {target_year_display} | Commits: {num_commits} | Repo: {repo_path}\n")

    success_count = 0
    start_time = time.time()

    if args.pattern:
        pattern = PATTERNS.get(args.pattern)
        if not args.silent:
            print(f"🎨 Drawing pattern: \033[1;35m{args.pattern}\033[0m")
        
        # We start the pattern at a reasonable column (e.g., week 10)
        start_col = 10
        for row_idx, row_str in enumerate(pattern):
            for col_idx, char in enumerate(row_str):
                if char != ' ':
                    # Commit multiple times for darkness
                    commits_per_cell = 5 if char == 'X' else 3
                    commit_date = get_date_from_grid(target_year_display, start_col + col_idx, row_idx)
                    
                    # Randomize time within that day
                    for _ in range(commits_per_cell):
                        h, m, s = random.randint(9, 17), random.randint(0, 59), random.randint(0, 59)
                        full_date = commit_date.replace(hour=h, minute=m, second=s)
                        if make_commit(full_date, repo_path, filename):
                                success_count += 1
        print(f"\nPattern generation complete.")
    else:
        for i in range(num_commits):
            commit_date = random_date_in_year(year_offset)
            if not args.silent:
                print(f"\r[{i+1}/{num_commits}] Working... 🏗️", end="", flush=True)
            if make_commit(commit_date, repo_path, filename):
                success_count += 1

    duration = time.time() - start_time
    if not args.silent:
        print(f"\n\n✅ Finished {success_count} commits in {duration:.2f}s.")

    should_push = args.push
    if not args.silent and not args.push:
        push_choice = input("\nDo you want to push to remote? (y/n, default n): ").lower().strip()
        should_push = (push_choice == 'y')

    if should_push:
        if not args.silent:
            print("Pushing to GitHub...")
        res = subprocess.run(["git", "push"], cwd=repo_path, capture_output=True, text=True)
        if res.returncode == 0:
            if not args.silent:
                print("\033[1;32m🚀 Successfully pushed!\033[0m")
        else:
            if not args.silent:
                print(f"\033[1;31m❌ Push failed:\033[0m {res.stderr.strip()}")

    if not args.silent:
        print("\n\033[1;32mThanks for using graph-greener! ✨\033[0m\n")

if __name__ == "__main__":
    main()