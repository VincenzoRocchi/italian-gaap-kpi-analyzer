# Installation Guide

There are several ways to get KPI CEE running on your system.

## Option 1: Using Pre-built Executables (Recommended for most users)

Pre-built versions of the application for Windows, macOS, and Linux are available for download from the [GitHub Releases page](https://github.com/yourusername/kpi_cee/releases). (Replace `yourusername/kpi_cee` with the actual repository path).

1.  Navigate to the Releases page.
2.  Download the archive (`.zip` or `.tar.gz`) for your operating system.
3.  Extract the archive.
4.  Run the `kpi_cee` executable (or `kpi_cee.app` on macOS) found within the extracted folder.

For detailed instructions on running the executables, please refer to the main [README.md#downloading-and-running-pre-built-executables](../README.md#downloading-and-running-pre-built-executables) of the project.

## Option 2: Running from Source Code (For developers or users comfortable with Python)

This method requires Python to be installed on your system (Python 3.12+ recommended).

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/kpi_cee.git # Replace with your actual repository path
    cd kpi_cee
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the `SECRET_KEY` environment variable:**
    Flask uses a `SECRET_KEY` for session management. For local use or development, you can set this environment variable to any non-empty string. This key helps secure session data.

    *   Example for macOS/Linux (in your terminal):
        ```bash
        export SECRET_KEY='your_chosen_local_key'
        ```
    *   Example for Windows (Command Prompt):
        ```bash
        set SECRET_KEY=your_chosen_local_key
        ```
    *   Example for Windows (PowerShell):
        ```bash
        $env:SECRET_KEY="your_chosen_local_key"
        ```
    Choose any string you like for local runs; it doesn't need to be cryptographically complex for this purpose.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application should then be accessible at `http://127.0.0.1:5000` in your web browser. 