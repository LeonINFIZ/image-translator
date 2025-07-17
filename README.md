# Image Translator

A web app that extracts text from images and translates it into any language — available both as plain text and visually overlaid on the original image.

## Features

-   **User Authentication**: Secure registration, login, and session management.
-   **Image OCR**: Extracts text from uploaded images using Tesseract.
-   **Text Translation**: Translates extracted text using Google Cloud Translate API.
-   **Intelligent Language Detection**: Automatically detects the source language to prevent redundant translations.
-   **Visual Overlay**: Displays the translated text directly on top of the original image.
-   **Translation History**: Logged-in users can view and manage their past translations.
-   **Responsive UI**: Clean user interface built with Bootstrap 5.

## Setup and Installation

### Prerequisites

-   Python 3.11+
-   Pipenv
-   Tesseract OCR

### 1. Clone the Repository

```bash
git clone https://github.com/LeonINFIZ/image-translator.git
cd image-translator
```

### 2. Set Up Environment and Dependencies

This project uses `pipenv` to manage dependencies.

```bash
# Install pipenv if you don't have it
pip install pipenv

# Install project dependencies from Pipfile and create a virtual environment
pipenv install --dev

# Activate the virtual environment
pipenv shell
```

### 3. Tesseract OCR Installation

Tesseract is an external dependency and must be installed on your system.

**For Windows:**
1.  Download the installer from Tesseract at UB Mannheim. It's recommended to download an installer for a version >= 5.
2.  Run the installer. During installation, make sure to select the language data you need (e.g., English, Russian, German, etc.). The application is currently configured to use English and Russian (`eng+rus`).
3.  After installation, you need to tell the Django application where to find Tesseract. Open `src/config/settings.py` and update the `TESSERACT_CMD` variable to point to your `tesseract.exe` location.
    ```python
    # src/config/settings.py
    TESSERACT_CMD = "C:/Program Files/Tesseract-OCR/tesseract.exe" # <-- Update this path
    ```

**For macOS/Linux:**
You can typically install Tesseract using a package manager.
```bash
# On Debian/Ubuntu
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-rus
```

### 4. Google Cloud Translate API Key

The application uses the Google Cloud Translation API. You will need a service account JSON credentials file.

1.  **Go to the Google Cloud Console** and create a new project.
2.  **Enable the Cloud Translation API** for your project.
3.  **Create a Service Account**: Go to `APIs & Services` > `Credentials`, click `+ CREATE CREDENTIALS`, and select `Service account`. Grant it the `Cloud Translation API User` role.
4.  **Generate a JSON Key**: From your new service account's `KEYS` tab, create a new JSON key. A `.json` file will be downloaded.
5.  **Use the Key**:
    -   Place the downloaded `.json` file in the **root directory** of this project.
    -   **Important**: The `.gitignore` file is already configured to prevent `*.json` files from being committed. **Never commit your credentials file to Git.**
    -   Finally, update the path in `src/config/settings.py` to match your key file's name.
    ```python
    # src/config/settings.py
    # Update this line with the name of your key file
    GOOGLE_APPLICATION_CREDENTIALS = BASE_DIR.parent / "your-credentials-file-name.json"
    ```

### 5. Run Migrations and Start the Server

```bash
# Apply database migrations
python src/manage.py migrate

# Start the development server
python src/manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.
