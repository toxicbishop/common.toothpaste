import os
import random
import subprocess
from datetime import datetime, timedelta

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

def random_date_in_year(year_offset):
    """
    Generates a random date within the specific target year.
    If target is current year, it ensures date is not in the future.
    """
    now = datetime.now()
    target_year = now.year + year_offset
    
    # Start of the target year (Jan 1st)
    start_date = datetime(target_year, 1, 1, 0, 0, 0)
    
    # End of the target year
    # If target is current year, end date is NOW (don't commit in future)
    # If target is past year, end date is Dec 31st
    if target_year == now.year:
        end_date = now
    else:
        end_date = datetime(target_year, 12, 31, 23, 59, 59)
    
    # Calculate time difference in seconds
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    
    if days_between_dates < 0:
        # Failsafe for rare edge cases
        return start_date

    random_seconds = random.randint(0, int(time_between_dates.total_seconds()))
    commit_date = start_date + timedelta(seconds=random_seconds)
    
    return commit_date

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    
    subprocess.run(["git", "add", filename], cwd=repo_path)
    
    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("="*60)
    print("🌱 Welcome to graph-greener - GitHub Contribution Graph Commit Generator 🌱")
    print("="*60)
    print("This tool will help you fill your GitHub contribution graph with custom commits.\n")

    num_commits = get_positive_int("How many commits do you want to make", 20)
    
    # New prompt for Year Selection
    current_year = datetime.now().year
    print(f"\nSelect Year Offset (Current year is {current_year})")
    print("Example: -1 selects " + str(current_year - 1))
    year_offset = get_year_offset("Enter year offset", -1)
    
    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")

    target_year_display = current_year + year_offset
    print(f"\nMaking {num_commits} commits in year: {target_year_display}")
    print(f"Repo: {repo_path}\nModifying file: {filename}\n")

    for i in range(num_commits):
        commit_date = random_date_in_year(year_offset)
        print(f"[{i+1}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename)

    print("\nPushing commits to your remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path)
    print("✅ All done! Check your GitHub contribution graph in a few minutes.\n")
    print("Tip: Use a dedicated repository for best results. Happy coding!")

if __name__ == "__main__":
    main()