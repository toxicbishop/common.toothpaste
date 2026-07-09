# GitHub Contribution Graph Generator

[![Python](https://img.shields.io/badge/python-3.12.x-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/toxicbishop/common.toothpaste/graphs/commit-activity)

A Python tool to automatically generate commits and fill your GitHub contribution graph with green squares. Perfect for showcasing consistent activity or filling in past activity gaps.

## Features

- **Custom Date Ranges**: Target specific years or offsets with ease.
- **Pattern Mode**: Draw amazing shapes like **Pacman** or **Hearts** on your graph!
- **Performance**: Optimized batch committing for rapid activity generation.
- **Automation Ready**: New `--silent` mode and CLI arguments for CI/CD integration.
- **Rich CLI**: Beautiful ANSI-colored interface for a premium experience.
- **Identity Check**: Automatically warns if your Git email doesn't match, ensuring your graph actually updates.

## Quick Start

### Prerequisites

- Python 3.12.x or higher
- Git installed and configured
- A GitHub repository (initialized with git)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/toxicbishop/common.toothpaste.git
cd common.toothpaste
```

2. Run the script:

```bash
python main.py
```

### Advanced Usage (CLI Flags)

Generate 100 random commits silently in the previous year:

```bash
python main.py --silent --commits 100 --offset -1 --push
```

### Pattern Mode (The Crowd Pleaser)

Fill your graph with a specific shape!

```bash
python main.py --pattern pacman --offset -1 --push
```

Available patterns: `pacman`, `heart`, `blocks`.

## How It Works

1. **Random Date Generation**: The script generates random dates within your specified year
2. **File Modification**: Each commit modifies the target file with a timestamp
3. **Git Backdating**: Commits are created with custom dates using `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`
4. **Automatic Push**: All commits are automatically pushed to your remote repository

## Customization

The script is designed to be easily customizable:

- Modify `make_commit()` to change commit messages
- Adjust `random_date_in_year()` for specific date ranges
- Customize the data written to files in `make_commit()`

## Important Notes

- **Use Responsibly**: This tool is for educational purposes. Don't misrepresent your actual contribution activity.
- **Dedicated Repository**: Consider using a separate repository to avoid cluttering your main projects.
- **Graph Update Delay**: GitHub may take a few minutes to update your contribution graph after pushing.
- **Time Zone**: Commits use your local system time zone.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is **free to use** - no license required! Feel free to use, modify, and distribute as you wish.

## Show Your Support

Give a star if this project helped you!

## Contact

- GitHub: [@toxicbishop](https://github.com/toxicbishop)

---

**Disclaimer**: This tool is for educational and personal use. Please use it ethically and in accordance with GitHub's terms of service.
