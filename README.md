# KPI CEE (KPI Calculator for Italian Financial Statements) - Beta Version 0.2.0

A web application that calculates Key Performance Indicators (KPIs) from financial statement data based on the Italian Civil Code (Codice Civile) article 2424 structure. 
**Note: This application is currently in Beta (Version 0.2.0).**

![License](https://img.shields.io/github/license/VincenzoRocchi/kpi_cee)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Flask Version](https://img.shields.io/badge/flask-3.1.0-blue)

## Overview

KPI CEE helps financial analysts, accountants, and business owners analyze financial statements by automatically calculating important financial ratios and KPIs from Italian GAAP-compliant financial statement data. The application follows the official structure defined by the Italian Civil Code (CEE format).

## Features

- **Italian GAAP Compliance**: Structured around the official CEE format (Art. 2424 Codice Civile)
- **Multiple KPI Calculations** (Current Ratio, Quick Ratio, Debt to Equity, etc.)
- **Intuitive Web Interface**: Select KPIs and input financial data through a clean, responsive UI
- **Detailed Results**: View calculated KPIs with interpretations and reference ranges

## Documentation

For detailed information on installation, usage, building from source, and project structure, please see the **[Full Documentation](./docs/README.md)**.

## Installation and Usage

For quick installation and usage instructions, please refer to the **[Installation Guide](./docs/01_installation.md)**.

## Downloading and Running Pre-built Executables

For users who do not want to install Python or manage dependencies, pre-built executables are available for Windows, macOS, and Linux.

1.  **Go to the [Releases Page](https://github.com/yourusername/kpi_cee/releases)** (replace `yourusername/kpi_cee` with your actual repository path).
2.  Find the latest release and download the appropriate archive file for your operating system:
    *   **Windows:** `kpi_cee-windows.zip` (containing the `kpi_cee` folder)
    *   **macOS:** `kpi_cee-macos.zip` (containing the `kpi_cee` folder, which might be `kpi_cee.app`)
    *   **Linux:** `kpi_cee-linux.tar.gz` (containing the `kpi_cee` folder)
3.  **Extract the downloaded archive.** This will create a `kpi_cee` folder.
4.  **Run the executable** located inside the extracted `kpi_cee` folder:
    *   **Windows:** Double-click `kpi_cee.exe` (inside the `kpi_cee` folder).
    *   **macOS:** 
        1.  Open the extracted `kpi_cee` folder. You should find `kpi_cee` (or `kpi_cee.app`).
        2.  If it's not an `.app` bundle, or if you prefer the terminal: Open Terminal, navigate to the extracted `kpi_cee` folder.
        3.  Make the file executable (if needed): `chmod +x kpi_cee`
        4.  Run: `./kpi_cee` or double-click the `kpi_cee` or `kpi_cee.app` file.
        5.  If you see an "unidentified developer" warning when double-clicking: Right-click (or Ctrl-click) the file, select "Open", and confirm. Alternatively, go to System Settings > Privacy & Security, scroll down, and look for an "Open Anyway" button.
    *   **Linux:** 
        1.  Open Terminal, navigate to the extracted `kpi_cee` folder.
        2.  Make the file executable: `chmod +x kpi_cee`
        3.  Run: `./kpi_cee`

The application should open in your default web browser automatically.

## Dependencies

- Python 3.12+
- Flask >=3.1.0

(See `requirements.txt` for exact pinned versions and `pyproject.toml` for base dependencies).

## License

This project is licensed under the terms in the `LICENSE` file (to be added - e.g., MIT License).

## Contributing

Contributions are welcome! Please see the [Contributing Guide](./docs/04_contributing.md) for more details.

## Development

To set up a development environment, please refer to the guides in our [Documentation](./docs/README.md), particularly:
*   [Installation (Running from Source)](./docs/01_installation.md#option-2-running-from-source-code)
*   [Building from Source](./docs/02_building_from_source.md)

```bash
# (After cloning and creating/activating virtual environment as per Installation docs)
# Run tests:
pytest
```

## CI/CD Pipeline (Automated Releases)

This project uses GitHub Actions to automate the building of executables and the creation of GitHub Releases. For more details, see the [workflow file](./.github/workflows/release.yml) and the [release notes generation script](./.github/workflows/release.yml) within the workflow.

**How to Create a New Release (and trigger the pipeline):**

1.  Ensure all your code changes are committed and pushed to your main branch.
2.  Create a new tag for your release. It's good practice to follow semantic versioning (e.g., `v0.3.0`).
    ```bash
    # Example for version 0.3.0
    git tag v0.3.0
    ```
3.  Push the tag to GitHub:
    ```bash
    git push origin v0.3.0 
    # Or push all tags: git push origin --tags
    ```
This will trigger the GitHub Actions workflow, which will build the executables and publish them in a new release on your GitHub repository's "Releases" page.

## Roadmap / Future Enhancements

(To be defined - consider adding items like: more KPIs, data import/export, charts, user accounts, etc.)
