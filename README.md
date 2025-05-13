# KPI CEE (KPI Calculator for Italian Financial Statements)

A web application that calculates Key Performance Indicators (KPIs) from financial statement data based on the Italian Civil Code (Codice Civile) article 2424 structure.

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

```bash
# Clone the repository
git clone https://github.com/yourusername/kpi_cee.git
cd kpi_cee

# Set up a Python 3.12 virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py
```

Then open your browser and navigate to http://127.0.0.1:5000/

1. Select the KPIs you want to calculate
2. Enter your financial statement data in the input form
3. View and interpret the calculated KPIs with provided guidance

## Project Structure

```
kpi_cee/
├── app.py             # Main Flask application
├── main.py            # Entry point script
├── static/            # Static assets
│   └── css/           # Stylesheets
│       └── custom.css # Custom styling
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── input.html     # Financial data input form
│   ├── results.html   # KPI results display
│   └── select_kpi.html # KPI selection page
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```

## Dependencies

- Python 3.12+
- Flask 3.1.0+

## License

This project is licensed under the terms in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Development

To set up a development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```
