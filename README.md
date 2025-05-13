# KPI CEE (KPI Calculator for Italian Financial Statements) - Version 0.2.8

<!-- Badges: License, Python Version, Flask Version -->
![License](https://img.shields.io/github/license/VincenzoRocchi/kpi_cee)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Flask Version](https://img.shields.io/badge/flask-3.1.0-blue)

**A web application to calculate Key Performance Indicators (KPIs) from Italian GAAP-compliant financial statements.**

## About The Project

KPI CEE is a Flask-based web tool designed for financial analysts, accountants, students, and business owners. It simplifies the analysis of financial statements by automatically calculating key financial ratios and KPIs based on the structure defined by the Italian Civil Code (Art. 2424 Codice Civile - CEE format).

This is an open-source project, free to use, modify, and distribute. Use it as a learning tool, a quick calculator, or adapt it to your specific needs!

## Features

- **Italian GAAP Compliance**: Structured around the official CEE format.
- **Multiple KPI Calculations**: Including Current Ratio, Quick Ratio, Debt to Equity, and more.
- **Intuitive Web Interface**: Easily select KPIs and input financial data.
- **Detailed Results**: View calculated KPIs with interpretations.

## Getting Started

There are two main ways to use KPI CEE:

### 1. Using Pre-built Releases (Windows & Linux)

Download ready-to-run executables for Windows and Linux. For macOS, running from source (see below) is the recommended method.

1.  Go to the **[Releases Page](https://github.com/VincenzoRocchi/kpi_cee/releases)**.
2.  Download the archive for your OS (e.g., `kpi_cee-windows.zip` or `kpi_cee-linux.tar.gz`).
3.  Extract the archive.
4.  Run the `kpi_cee` executable found inside the extracted folder.

For more detailed OS-specific instructions, see the **[Installation Guide in our Docs](./docs/01_installation.md)** (Note: macOS executable instructions may be outdated).

### 2. Running from Source Code (Recommended for macOS, also for Windows/Linux)

This gives you more flexibility, is the best way to get the latest updates, and is great if you want to see the code or modify it.

#### Installing `uv` (Recommended Package Installer)

`uv` is an extremely fast Python package installer and project manager, written in Rust. It can be used as a significantly faster alternative to `pip` and `venv`.

*   **macOS and Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
*   **Windows (PowerShell):**
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
*   Alternatively, install via pip: `pip install uv` or `pipx install uv`.

For more installation options, see the [official `uv` installation guide](https://docs.astral.sh/uv/getting-started/installation/).

#### Setup Steps

1.  **Prerequisites:**
    *   **Python:** Version 3.10 or newer is recommended.
        *   **macOS:** The easiest way to install Python is using [Homebrew](https://brew.sh/). Once Homebrew is installed, run: `brew install python`
        *   **Windows/Linux:** Download from the [official Python website](https://www.python.org/downloads/) or use your system's package manager (e.g., `apt` on Debian/Ubuntu).
    *   **Git:** To clone the repository. ([Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/VincenzoRocchi/kpi_cee.git
    cd kpi_cee
    ```

3.  **Set up a Python virtual environment:**
    *   **Using `uv` (Recommended):**
        ```bash
        uv venv
        # Activate the environment (uv will show the command, usually:)
        # On macOS/Linux: source .venv/bin/activate
        # On Windows: .venv\Scripts\activate
        ```
    *   **Using standard `venv`:**
        ```bash
        python -m venv venv
        # On Windows: venv\Scripts\activate
        # On macOS/Linux: source venv/bin/activate
        ```

4.  **Install dependencies:**
    *   **Using `uv` (Recommended, installs from `pyproject.toml`):
        ```bash
        uv pip install -e .
        ```
    *   **Using `pip` (installs Flask from `requirements.txt`):
        ```bash
        pip install -r requirements.txt 
        # Note: For development tools like pytest and PyInstaller, 
        # ensure they are installed separately if not using the uv command above,
        # or if they are removed from pyproject.toml's main dependencies in the future.
        ```

5.  **Set the `SECRET_KEY` environment variable (Optional for Local Development):**
    Flask sessions use a `SECRET_KEY`. The application will generate a temporary one if `SECRET_KEY` is not set in your environment. For persistent sessions or if you prefer to set it explicitly for local development:
    *   macOS/Linux (in your terminal):
        ```bash
        export SECRET_KEY='my_local_dev_key'
        ```
    *   Windows (Command Prompt):
        ```bash
        set SECRET_KEY=my_local_dev_key
        ```
    (This key is for session security; it doesn't need to be overly complex for local runs.)

6.  **Run the application:**
    ```bash
    python app.py
    ```
    Open your browser and go to `http://127.0.0.1:5001`.

For further details, refer to the **[Installation Guide for Running from Source](./docs/01_installation.md#option-2-running-from-source-code)**.

## Building Your Own Executable

If you've modified the code or want to package it yourself, you can build your own executables using PyInstaller.

Detailed instructions are available in the **[Building from Source Guide](./docs/02_building_from_source.md)**.

## Documentation

For more in-depth information, including project structure and contribution guidelines, please visit our main **[Documentation Hub](./docs/README.md)**.

## Dependencies

- Python 3.10+ (3.12 recommended)
- Flask >=3.0.0
(See `requirements.txt` for the exact Flask version).

## License

This project is licensed under the terms detailed in the [LICENSE](./LICENSE) file.

## Contributing

Contributions, suggestions, and bug reports are welcome! Please see our **[Contributing Guide](./docs/04_contributing.md)** for more details.

## Development

If you're contributing or modifying the code:

*   Follow the "Running from Source" steps above to set up your environment, preferably using `uv`.
*   If you used `uv pip install -e .` or installed the project from `pyproject.toml`, development tools like `pytest` (for testing) and `PyInstaller` (for building executables, if you choose to) are already installed as they are listed in `pyproject.toml`.
*   Run tests using Pytest:
    ```bash
    pytest
    ```

## CI/CD Pipeline (Automated Releases)

This project uses GitHub Actions to automatically build executables for Windows and Linux, and create GitHub Releases when a new version tag (e.g., `v0.3.0`) is pushed. See the [workflow file](./.github/workflows/release.yml) for details.

## Roadmap / Future Enhancements

(To be defined - consider adding items like: more KPIs, data import/export, charts, user accounts, etc.)
