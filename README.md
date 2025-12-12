# SourceUp
**SourceUp** is a desktop app that bridges your **Zotero** library with **Microsoft Word**'s native bibliography system.

### Who is SourceUp for, and why use it?

If you manage your references in **Zotero** but write in **Microsoft Word**, you quickly hit a wall:

- Word can’t read your Zotero library directly.
- Zotero and Word use different bibliography formats (CSL vs BibXML).
- You end up duplicating references, copy-pasting, or manually keeping multiple tools in sync.

**SourceUp** fixes this by:

- Reading your Zotero library directly.
- Generating a clean, Word-compatible **BibXML** file, using the best possible mapping from Zotero fields to Word’s format.
- Letting you import it into Word’s native bibliography system in a few clicks.

SourceUp is designed for **students, researchers, and academic writers** who want:
 
- Zotero as their single source of truth for references.
- Microsoft Word as their main writing tool.
- Fewer manual steps, less copy-pasting, and a cleaner, more reliable bibliography.

## 📦 Installation
### Option 1: Prebuilt Packages (Recommended)

If you don’t want to build from source, you can download the latest **Windows** beta build from the [Releases page](https://github.com/iredstonne/SourceUp/releases).

Prebuilt packages are currently **only available for Windows**. Support for **macOS** packages is planned for a future release.
On macOS and Linux, use **Option 2: Build From Source**.

### Option 2: Build From Source (Advanced)

This option is intended for **developers** and for running SourceUp on **macOS** or **Linux**.  
It also works well on **Windows** if you prefer a source-based, fully controllable setup (for example, when developing or testing new features).

Building from source gives you:
- Full control over the Python environment.
- The ability to track the latest changes from `main` or `dev`.
- Easier debugging and local development.

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

- Open an issue to report a bug, suggest an improvement, or propose a new feature.
- Submit a pull request with a focused change (bugfix, feature, or refactor).

When you open a PR, try to include a short description of:

- What you changed.
- Why you changed it.

This helps keep the project maintainable over time, even for small contributions.
