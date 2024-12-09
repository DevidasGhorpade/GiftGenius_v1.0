# Gift Genius v1.0

Gift Genius allows users to quickly make the best-informed decision when purchasing gift cards. Options include a wide selection of gift cards from different retailers and brands, gift card customization, and digital or physical card delivery options.

This E-Gift Commerce Portal built using Django and Tailwind CSS.

## Table of Contents

- [Project Setup](#project-setup)
  - [For macOS/Linux](#for-macoslinux)
  - [For Windows](#for-windows)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## Project Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtualenv (optional, but recommended)
- Node.js (for Tailwind CSS)

### For macOS/Linux

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd e-giftcard-portal
    ```

2. **Create a Virtual Environment**:
    (Optional, but recommended)
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Node.js (if not installed)**:
    Follow [this guide](https://nodejs.org/en/download/) to install Node.js.

5. **Install Tailwind CSS**:
    Install Tailwind CSS as a PostCSS plugin by running:
    ```bash
    npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
    ```

6. **Run the Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

7. **Create your Admin account**:
    ```bash
    python manage.py createsuperuser
    ```

### For Windows

1. **Clone the Repository**:
    Open PowerShell:
    ```powershell
    git clone <repository-url>
    cd e-giftcard-portal
    ```

2. **Create a Virtual Environment**:
    (Optional, but recommended)
    ```powershell
    python -m venv env
    env\Scripts\activate
    ```

3. **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

4. **Install Node.js (if not installed)**:
    Follow [this guide](https://nodejs.org/en/download/) to install Node.js.

5. **Install Tailwind CSS**:
    Install Tailwind CSS as a PostCSS plugin by running:
    ```powershell
    npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
    ```

6. **Run the Migrations**:
    ```powershell
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Create your Admin account**:
    ```powershell
    python manage.py createsuperuser
    ```

---

## Running the Application

### Load giftcard fixtures into database

```shell
# Load fixtures from giftcards app, fixtures directory, load_data.json:
python manage.py loaddata load_data
```

### Collect all static files into single location defined by STATIC_ROOT (optional)

```shell
# Not necessary for Django test environment, but recommended for production:
python manage.py collectstatic
```

### Start the Django development server

```shell
# Once setup complete, this can be used for developer testing only:
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/.
