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
- **Multiple KPI Calculations**:
  - Current Ratio (Indice di Liquidità Corrente)
  - Quick Ratio (Indice di Liquidità Immediata)
  - Cash Ratio (Indice di Cassa)
  - Debt to Equity Ratio (Rapporto Debiti/Patrimonio Netto)
  - Debt Ratio (Rapporto di Indebitamento Totale)
  - Working Capital (Capitale Circolante Netto)
- **Intuitive Web Interface**: Select KPIs and input financial data through a clean, responsive UI
- **Detailed Results**: View calculated KPIs with interpretations and reference ranges

## Installation

Ensure you have Python 3.12 or higher installed.

```bash
# Clone the repository
git clone https://github.com/yourusername/kpi_cee.git # Replace with your actual username/repo
cd kpi_cee

# Set up a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# IMPORTANT: Set the Flask Secret Key
# For development, you can set it in your terminal:
# On Linux/macOS:
# export SECRET_KEY='your_very_secret_random_key_here'
# On Windows (Command Prompt):
# set SECRET_KEY=your_very_secret_random_key_here
# On Windows (PowerShell):
# $env:SECRET_KEY="your_very_secret_random_key_here"
# For production, use a proper secrets management solution.
```

## Usage

```bash
# Ensure your virtual environment is activated and SECRET_KEY is set
# Then run the application:
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000/`

1.  Select the KPIs you want to calculate.
2.  Enter your financial statement data in the input form.
3.  View and interpret the calculated KPIs with provided guidance.

## Project Structure (Version 0.2.0)

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
├── pyproject.toml             # Project metadata and dependencies (PEP 517/518)
├── requirements.txt           # Pinned dependencies for deployment/reproducibility
└── README.md                  # This file
# Recommended: Add .gitignore, LICENSE
```

## Dependencies

- Python 3.12+
- Flask >=3.1.0

(See `requirements.txt` for exact pinned versions and `pyproject.toml` for base dependencies).

## License

This project is licensed under the terms in the `LICENSE` file (to be added - e.g., MIT License).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Consider creating an issue first to discuss significant changes.

## Development

To set up a development environment:

```bash
# (After cloning and creating/activating virtual environment as per Installation)
# Install development dependencies (if you define them in pyproject.toml or have a separate dev-requirements.txt)
# For example, ensure pytest is installed (it's now in requirements.txt):
# pip install pytest 

# Run tests:
pytest
```

## Roadmap / Future Enhancements
