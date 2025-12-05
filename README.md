# SourceUp
**SourceUp** is a desktop app that bridges your **Zotero** library with **Microsoft Word** by exporting your references to a Word-friendly bibliography format (**BibXML**)

## 📦 Installation
### Option 1: Prebuilt Packages (coming soon)

If you don’t want to build from source, you’ll be able to download a prebuilt package for **Windows** from the [Releases page](https://github.com/iredstonne/SourceUp/releases).

### Option 2: Build From Source

This is the recommended way to run SourceUp on **non-Windows platforms** (and it also works on Windows, of course).

#### Requirements
- [Python 3.12](https://www.python.org/downloads/release/python-3120) (tested)
- [Poetry](https://python-poetry.org)

### Setup
Clone the repository, install dependencies, and run it:

```bash
git clone https://github.com/iredstonne/SourceUp.git
cd SourceUp
poetry install
poetry run sourceup
```

## Contributing
Contributions are welcome! 

You can:

- Open an issue to report a bug, suggest an improvement, or propose a new feature
- Submit a pull request with a focused change (bugfix, feature, or refactor)

When you open a PR, try to include a short description of:

- What you changed
- Why you changed it

This helps keep the project maintainable over time, even for small contributions
