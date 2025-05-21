# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4 Beta] - 2025-05-21

### Added
- **UI (KPI Selection Page):**
    - Added "Select All" and "Deselect All" buttons for KPI selection.
    - Added a "Procedi all'Inserimento Dati" button at the top of the KPI selection page, positioned on the same horizontal line as the "Select/Deselect All" buttons (select/deselect on the left, proceed on the right).

### Changed
- **Refactoring:** Split the main `app_logic/constants.py` file into multiple, more focused configuration files (`balance_sheet_config.py`, `kpi_config.py`, `mappings_config.py`, `kpi_requirements_logic.py`) to improve code organization and maintainability. The original `constants.py` now imports from these new files.

### Fixed
- **UI (Print):** Resolved vertical overlap issue in the KPI summary print view, ensuring KPI cards stack correctly.

## [0.3.3 Beta] - 2025-05-21

### Added
- Implemented server-side session management using Flask-Session to resolve browser cookie size limitations
- Added functionality to preserve user input data when validation errors occur
- Added visual feedback for validation errors by highlighting invalid input fields in red
- Improved user experience with field-specific error messages that clear when the user starts typing

### Fixed
- Resolved issue with data not being kept in memory when validation errors occur
- Updated deprecated datetime.utcnow() to use timezone-aware datetime.now(UTC)
- Fixed print layout issues with overlapping KPI tiles when printing complete reports
- Improved position name display in results page to avoid "Nome non trovato" messages

## [0.3.2 Beta] - 2025-05-14

### Changed
- **Core Architecture:** Migrated CEE balance sheet position keys from integers to strings throughout the application (e.g., in `app_logic/constants.py`, `app.py`, `templates/input.html`). This foundational change allows for more flexible position definitions, such as `'39'` for current and `'39.NCA'` for non-current assets.
- Refined `quick_ratio` definition in `app_logic/constants.py` for closer alignment with standard financial practices by ensuring the numerator correctly combines liquid assets, cash, and current financial assets, and the denominator uses current liabilities.

### Fixed
- Resolved `NameError` in `app_logic/constants.py` where `_kpi_req_total_assets` was used before its definition; corrected by reordering variable initializations.
- Addressed various `TypeError` and `KeyError` issues in `app.py` and `app_logic/constants.py` stemming from the transition to string-based position keys.
- Corrected logic in `app.py` for building `required_structure` to accurately handle nested dictionary structures for receivables in `templates/input.html` after the string key migration.
- General review and confirmation of other KPI definitions in `app_logic/constants.py` against financial standards.

## [0.3.1] - 2025-05-14 
### Added
- New KPIs: `debt_to_equity_excl_tfr` and `debt_ratio_excl_tfr` to provide financial insights excluding the Employee Severance Indemnity (TFR).

### Changed
- Updated `app_logic/constants.py` to include `POS_TOTAL_LIABILITIES_EXCL_TFR` and new entries in `KPI_REQUIREMENTS` for the TFR-exclusive KPIs.
- Modified `app_logic/calculator.py` to implement the calculation logic for `debt_to_equity_excl_tfr` and `debt_ratio_excl_tfr`.

## [0.3.0 Beta] - 2025-05-14

### Added
- **PDF Export Functionality:**
  - Users can now print the KPI results page to PDF directly from their browser.
  - Added two print modes accessible via buttons on the results page:
    - **Stampa Riepilogo KPI:** Prints a summary of the calculated KPI values, formatted for a clean, full-page overview.
    - **Stampa Report Completo:** Prints the KPI results followed by the detailed input data used for each KPI (in a two-column layout under each respective KPI card) and the "Controllo Quadratura" section at the end.
  - Implemented client-side printing using `window.print()` and CSS `@media print` rules to style the output for both modes, ensuring a good user experience without server-side PDF generation dependencies.
- Updated application version to 0.3.0 Beta in `app.py` and relevant documentation.

### Changed
- Minor CSS adjustments for print layout and on-screen display consistency.

### Fixed
- Resolved various template rendering issues related to the print functionality development.