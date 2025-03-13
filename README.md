# <div align="center">🚀 SVCS: Simplified Version Control System 🚀</div>

<div align="center">

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

<div align="center">

```
 ____   __     __  ____   ____
/ ___) /  \   /  \/ ___) / ___)
\___ \(  O ) (  O )\___ \\___ \
(____/ \__/   \__/(____/(____/
```

**A lightweight, blazing-fast, and elegant version control system for all your text files**

[Features](#✨-features) •
[Installation](#🔧-installation) •
[Quick Start](#🚀-quick-start) •
[Documentation](#📚-documentation) •
[Examples](#💡-examples) •
[Contributing](#🤝-contributing) •
[License](#📄-license)

</div>

---

## 🌟 Overview

**SVCS** is a modern, Python-based version control system designed with simplicity and efficiency in mind. Whether you're a developer, writer, or anyone who works with text files, SVCS offers intuitive version tracking without the complexity of traditional VCS solutions.

> "Simple tools should solve complex problems simply." — SVCS Philosophy

## ✨ Features

- **📁 Intelligent File Tracking** — Smart detection and monitoring of changes in your text files
- **📊 Powerful Versioning** — Create timestamped snapshots with unique identifiers
- **🔍 Advanced Diff Engine** — Crystal-clear visual representation of changes between versions
- **⏳ Time Travel** — Seamlessly navigate through your project's history
- **🖥️ Developer-Friendly CLI** — Intuitive commands that feel natural and predictable
- **🚀 Lightweight & Fast** — Minimal system footprint with optimized performance
- **📝 Text-File Focus** — Specialized handling for over 15 common text file formats

## 🔧 Installation

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Method 1: From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/svcs.git

# Navigate to the project directory
cd svcs

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Using pip (Coming Soon)

```bash
pip install svcs
```

## 🚀 Quick Start

### Initialize a Repository

```bash
python -m cli init
```

This creates a `.svcs` directory to store all version control information.

### Track Your First Changes

1. Make changes to your files
2. Create a version (commit) with your changes:

```bash
python -m cli commit "Initial commit - Add project structure"
```

## 📚 Documentation

### Core Commands

| Command    | Description                      | Example                                   |
| ---------- | -------------------------------- | ----------------------------------------- |
| `init`     | Initialize a new SVCS repository | `python -m cli init`                      |
| `commit`   | Create a new version             | `python -m cli commit "Fix bug in login"` |
| `status`   | Check for changes                | `python -m cli status`                    |
| `log`      | View version history             | `python -m cli log`                       |
| `diff`     | Compare versions                 | `python -m cli diff abc123 def456`        |
| `checkout` | Restore to a version             | `python -m cli checkout abc123`           |

### Advanced Usage

#### Comparing Specific Files Between Versions

```bash
python -m cli diff --file path/to/file.py abc123 def456
```

#### Viewing Detailed Version Information

```bash
python -m cli log --verbose
```

#### Selective Committing

```bash
python -m cli commit --files file1.py,file2.py "Update utility functions"
```

## 💡 Examples

### Tracking a Website Project

```bash
# Initialize in your project folder
cd my-website
python -m cli init

# After adding some HTML and CSS
python -m cli commit "Initial version of homepage"

# After making more changes
python -m cli status
# Output: Modified: index.html, styles.css

# Commit the changes
python -m cli commit "Improve responsive design"

# Compare with previous version
python -m cli diff
```

### Managing a Research Paper

```bash
# Initialize in your paper directory
cd research-paper
python -m cli init

# After drafting introduction
python -m cli commit "Draft introduction section"

# After advisor feedback
python -m cli commit "Revise introduction based on feedback"

# See what changed
python -m cli diff HEAD~1 HEAD
```

## 🔧 Supported File Types

SVCS is optimized for tracking the following text file formats:

**Development**

- 🐍 Python (.py)
- 🌐 JavaScript (.js)
- 📄 HTML (.html)
- 🎨 CSS (.css)
- 📊 JSON/XML (.json, .xml)
- ☕ Java (.java)
- 🔧 C/C++ (.c, .cpp, .h)

**Documentation & Data**

- 📝 Markdown (.md)
- 📄 Text (.txt)
- 📊 CSV (.csv)
- ⚙️ Configuration files (.yaml, .yml, .toml, .ini, .cfg)

**Scripts**

- 💻 Shell scripts (.sh, .bat, .ps1)

## 🧠 Under the Hood

SVCS employs several sophisticated components that work together seamlessly:

- **FileTracker** — Uses SHA-256 hashing to efficiently detect file changes
- **VersionManager** — Implements a directed acyclic graph (DAG) for version history
- **DiffEngine** — Features a refined algorithm for generating human-readable diffs
- **CLI** — Built with Click library for a polished user experience

## 🏗️ Project Structure

```
SVCS/
├── filetracker.py    # File change detection system
├── versionmanager.py # Version creation and management
├── diffengine.py     # File comparison utilities
├── utils.py          # Helper functions
└── cli.py            # Command-line interface
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b amazing-feature`
3. **Commit** your changes: `git commit -m 'Add some amazing feature'`
4. **Push** to your branch: `git push origin amazing-feature`
5. **Submit** a pull request

Please check our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- The Click library team for their excellent CLI framework
- All our contributors and supporters

---

<div align="center">
  <sub>Built with ❤️ by TheRealSaiTama</sub>
</div>
