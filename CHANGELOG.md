# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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