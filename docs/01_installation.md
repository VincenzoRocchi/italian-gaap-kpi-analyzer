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
    For security, Flask sessions require a secret key. For development, you can set this in your terminal:
    *   macOS/Linux:
        ```bash
        export SECRET_KEY='a_very_secret_and_random_key_should_go_here'
        ```
    *   Windows (Command Prompt):
        ```bash
        set SECRET_KEY=a_very_secret_and_random_key_should_go_here
        ```
    *   Windows (PowerShell):
        ```bash
        $env:SECRET_KEY="a_very_secret_and_random_key_should_go_here"
        ```
    **Note:** For production, use a proper method for managing secrets.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application should then be accessible at `http://127.0.0.1:5000` in your web browser. 