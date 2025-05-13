# Project Structure (Version 0.2.0)

This document outlines the main directories and files in the KPI CEE project.

```
kpi_cee/
├── app.py                     # Main Flask application runner and routes
├── app_logic/                 # Core application logic and data
│   ├── __init__.py            # Makes app_logic a Python package
│   ├── calculator.py          # KPI calculation functions
│   ├── constants.py           # Data definitions (balance sheet, KPIs, etc.)
│   └── validators.py          # Input validation functions
├── static/                    # Static assets (CSS, JS, images)
│   └── css/
│       └── custom.css
├── templates/                 # HTML templates for the web interface
│   ├── base.html              # Base template with common layout
│   ├── input.html             # Financial data input form
│   ├── results.html           # KPI results display
│   ├── select_kpi.html        # KPI selection page
│   └── partials/              # (If you add partial templates)
├── tests/                     # Test suite for the application
│   ├── __init__.py            # Makes tests a Python package
│   └── test_calculator.py     # Tests for KPI calculations
├── .github/                   # GitHub Actions workflows
│   └── workflows/
│       └── release.yml        # Workflow for building and releasing executables
├── docs/                      # Project documentation
│   ├── README.md              # Overview of documentation
│   ├── 01_installation.md     # How to install and run
│   ├── 02_building_from_source.md # How to build executables
│   ├── 03_project_structure.md# This file
│   └── 04_contributing.md     # Guidelines for contributors (placeholder)
├── pyproject.toml             # Project metadata and dependencies (PEP 517/518)
├── requirements.txt           # Pinned dependencies for deployment/reproducibility
├── README.md                  # Main project README
└── .gitignore                 # Specifies intentionally untracked files that Git should ignore
# Recommended: Add LICENSE
```

## Key Components:

*   **`app.py`**: The entry point for the Flask web application. It handles routing, request processing, and interactions with the `app_logic` components.
*   **`app_logic/`**: This directory is the heart of the application's business logic.
    *   `constants.py`: Defines all fixed data structures, such as the balance sheet format, KPI definitions, available KPIs, position names, etc.
    *   `calculator.py`: Contains functions for performing the actual KPI calculations and validating the overall balance sheet data.
    *   `validators.py`: Provides functions to validate user inputs, such as financial data and KPI selections.
*   **`templates/`**: Contains HTML templates used by Flask to render the web pages.
*   **`static/`**: Holds static files like CSS stylesheets, JavaScript files (if any), and images.
*   **`tests/`**: Contains automated tests for the application, primarily focusing on the calculation logic in `calculator.py`.
*   **`.github/workflows/release.yml`**: Defines the CI/CD pipeline using GitHub Actions to automatically build executables for Windows, macOS, and Linux, and create a GitHub Release with these assets whenever a new version tag (e.g., `v0.2.1`) is pushed.
*   **`docs/`**: Contains detailed documentation for users and developers. 