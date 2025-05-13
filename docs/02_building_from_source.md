# Building from Source

If you want to create your own executable builds from the source code, you can use PyInstaller. This is useful if you've made modifications to the code or want to build for a specific environment not covered by the pre-built releases.

## Prerequisites

1.  **Python 3.12+** installed and added to your system's PATH.
2.  **Project cloned** and you are in the project's root directory.
3.  **Virtual environment** created and activated.
4.  **Dependencies installed** by running `pip install -r requirements.txt` (this includes PyInstaller).

## Build Command

Once the prerequisites are met, run the following command from the project's root directory:

```bash
python -m PyInstaller --name kpi_cee \
    --onedir \
    --noconsole \
    --add-data "templates<SEPARATOR>templates" \
    --add-data "static<SEPARATOR>static" \
    app.py
```

**Important:** Replace `<SEPARATOR>` with the correct path separator for your operating system:
*   **macOS/Linux:** Use `:` (colon)
    ```bash
    # Example for macOS/Linux:
    python -m PyInstaller --name kpi_cee \
        --onedir \
        --noconsole \
        --add-data "templates:templates" \
        --add-data "static:static" \
        app.py
    ```
*   **Windows:** Use `;` (semicolon)
    ```bash
    # Example for Windows:
    python -m PyInstaller --name kpi_cee ^
        --onedir ^
        --noconsole ^
        --add-data "templates;templates" ^
        --add-data "static;static" ^
        app.py
    ```
    (Note: `^` is used for line continuation in Windows Command Prompt. If using PowerShell, you might use backticks `` ` `` or write it as a single line.)

## Output

After a successful build, you will find the packaged application in the `dist/kpi_cee` directory.

*   On **Windows**, this will contain `kpi_cee.exe` and other supporting files.
*   On **macOS**, this will usually be a `kpi_cee.app` bundle (if `--noconsole` or `--windowed` is used) or a folder containing the `kpi_cee` executable.
*   On **Linux**, this will be a folder containing the `kpi_cee` executable and its dependencies.

## Troubleshooting Build Issues

*   Ensure all dependencies, especially PyInstaller, are up to date (`pip install --upgrade PyInstaller`).
*   Check the PyInstaller warnings and error messages for clues. Common issues involve missing hidden imports or data files.
*   Consult the [PyInstaller documentation](https://pyinstaller.readthedocs.io/en/stable/) for advanced troubleshooting. 