# SourceUp
**SourceUp** is a desktop app that bridges your **Zotero** library with **Microsoft Word** by exporting your references to a Word-friendly bibliography format (**BibXML**)

## 📦 Installation
### Option 1: Prebuilt Packages (Recommended)

If you don’t want to build from source, you can download the latest **Windows** beta build from the [Releases page](https://github.com/iredstonne/SourceUp/releases).

Prebuilt packages are currently **only available for Windows**. Support for **macOS** packages is planned for a future release.
On macOS and Linux, use **Option 2: Build From Source**.

### Option 2: Build From Source (Advanced)

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
Contributions are welcome! **English is required** for issues, pull requests, and code comments so the project stays accessible to everyone.

You can:

- Open an issue to report a bug, suggest an improvement, or propose a new feature
- Submit a pull request with a focused change (bugfix, feature, or refactor)

When you open a PR, try to include a short description of:

- What you changed
- Why you changed it

This helps keep the project maintainable over time, even for small contributions
