# KPI CEE (KPI Calculator for Italian Financial Statements) - Beta Version 0.2.0

<!-- Badges: License, Python Version, Flask Version -->
![License](https://img.shields.io/github/license/VincenzoRocchi/kpi_cee) <!-- Replace with your actual repo path if different -->
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

### 1. Using Pre-built Releases (Recommended for Quick Use)

Download ready-to-run executables for your operating system.

1.  Go to the **[Releases Page](https://github.com/yourusername/kpi_cee/releases)** (replace `yourusername/kpi_cee` with your actual repository path).
2.  Download the archive for your OS (e.g., `kpi_cee-windows.zip`).
3.  Extract the archive.
4.  Run the `kpi_cee` executable (or `kpi_cee.app` on macOS) found inside the extracted folder.

For more detailed OS-specific instructions, see the **[Installation Guide in our Docs](./docs/01_installation.md)**.

### 2. Running from Source Code

This gives you more flexibility and is great if you want to see the code or modify it.

1.  **Prerequisites:**
    *   Python 3.12+
    *   Git

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/kpi_cee.git # Replace with your repo path
    cd kpi_cee
    ```

3.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set the `SECRET_KEY` environment variable:**
    Flask sessions require a `SECRET_KEY`. For local use, you can set this environment variable to any non-empty string. For example:
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
    Open your browser and go to `http://127.0.0.1:5000`.

For further details, refer to the **[Installation Guide for Running from Source](./docs/01_installation.md#option-2-running-from-source-code)**.

## Building Your Own Executable

If you've modified the code or want to package it yourself, you can build your own executables using PyInstaller.

Detailed instructions are available in the **[Building from Source Guide](./docs/02_building_from_source.md)**.

## Documentation

For more in-depth information, including project structure and contribution guidelines, please visit our main **[Documentation Hub](./docs/README.md)**.

## Dependencies

- Python 3.12+
- Flask >=3.1.0
(See `requirements.txt` for exact versions).

## License

This project is licensed under the terms in the `LICENSE` file (e.g., MIT License - to be added). See `LICENSE` for more information.

## Contributing

Contributions, suggestions, and bug reports are welcome! Please see our **[Contributing Guide](./docs/04_contributing.md)** for more details.

## Development

If you're contributing or modifying the code:

*   Follow the "Running from Source" steps above to set up your environment.
*   Run tests using Pytest:
    ```bash
    pytest
    ```

## CI/CD Pipeline (Automated Releases)

This project uses GitHub Actions to automatically build executables and create GitHub Releases when a new version tag (e.g., `v0.3.0`) is pushed. See the [workflow file](./.github/workflows/release.yml) for details.

## Roadmap / Future Enhancements

(To be defined - consider adding items like: more KPIs, data import/export, charts, user accounts, etc.)
