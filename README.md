# 🌱 GitHub Contribution Graph Generator

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/toxicbishop/common.toothpaste/graphs/commit-activity)

A Python tool to automatically generate commits and fill your GitHub contribution graph with green squares. Perfect for showcasing consistent activity or filling in past activity gaps.

## ✨ Features

- 🎯 **Custom Date Ranges**: Target specific years (current, previous, or any year offset)
- 🔢 **Flexible Commit Count**: Generate as many or as few commits as you want
- 📅 **Smart Date Generation**: Automatically generates commits only within valid date ranges
- 🚀 **Automated Git Operations**: Handles all git operations (add, commit, push)
- 🎨 **Interactive CLI**: User-friendly prompts with sensible defaults
- 📁 **Configurable**: Choose your own repository path and commit file

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Git installed and configured
- A GitHub repository (initialized with git)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/toxicbishop/common.toothpaste.git
cd common.toothpaste
```

1. Run the script:

```bash
python main.py
```

## 📖 Usage

When you run the script, you'll be prompted for:

1. **Number of commits**: How many commits to generate (default: 20)
2. **Year offset**: Which year to target
   - `0` = Current year (2026)
   - `-1` = Previous year (2025)
   - `-2` = Two years ago (2024)
3. **Repository path**: Where your git repository is located (default: current directory)
4. **Filename**: Which file to modify for commits (default: `data.txt`)

### Example Session

```text
============================================================
🌱 Welcome to graph-greener - GitHub Contribution Graph Commit Generator 🌱
============================================================
This tool will help you fill your GitHub contribution graph with custom commits.

How many commits do you want to make (default 20): 50

Select Year Offset (Current year is 2026)
Example: -1 selects 2025
Enter year offset (default -1): -1

Enter the path to your local git repository (default current directory): 
Enter the filename to modify for commits (default data.txt): 

Making 50 commits in year: 2025
Repo: .
Modifying file: data.txt

[1/50] Committing at 2025-03-15 14:32:18
[2/50] Committing at 2025-07-22 09:45:33
...
[50/50] Committing at 2025-11-08 21:17:42

Pushing commits to your remote repository...
✅ All done! Check your GitHub contribution graph in a few minutes.

Tip: Use a dedicated repository for best results. Happy coding!
```

## ⚙️ How It Works

1. **Random Date Generation**: The script generates random dates within your specified year
2. **File Modification**: Each commit modifies the target file with a timestamp
3. **Git Backdating**: Commits are created with custom dates using `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`
4. **Automatic Push**: All commits are automatically pushed to your remote repository

## 🎨 Customization

The script is designed to be easily customizable:

- Modify `make_commit()` to change commit messages
- Adjust `random_date_in_year()` for specific date ranges
- Customize the data written to files in `make_commit()`

## ⚠️ Important Notes

- **Use Responsibly**: This tool is for educational purposes. Don't misrepresent your actual contribution activity.
- **Dedicated Repository**: Consider using a separate repository to avoid cluttering your main projects.
- **Graph Update Delay**: GitHub may take a few minutes to update your contribution graph after pushing.
- **Time Zone**: Commits use your local system time zone.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is **free to use** - no license required! Feel free to use, modify, and distribute as you wish.

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

## 📬 Contact

- GitHub: [@toxicbishop](https://github.com/toxicbishop)

---

**Disclaimer**: This tool is for educational and personal use. Please use it ethically and in accordance with GitHub's terms of service.
