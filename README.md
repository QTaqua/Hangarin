# Hangarin (Task Manager)

A multi-user task management web application built with Django, featuring a dark Japanese minimalist aesthetic, Progressive Web App (PWA) support, OAuth authentication via Google and GitHub, and seed data generation.

**Developer:** Jabriel Encarnacion

---

## Features

* **Authentication & Connections**: Complete user authentication powered by `django-allauth`, supporting Google and GitHub OAuth 2.0 integration alongside account management/linking.
* **Minimalist Japanese UI**: Customized dark-mode aesthetic utilizing deep canvas tones (`#121212`), high-contrast dark cards (`#1e1e1e`), serif headings, and crimson accents (`#e63946`).
* **Progressive Web App (PWA)**: Installable as a native app on desktop and mobile devices with offline capabilities, cached assets, and service worker integration powered by `django-pwa`.
* **Task Management**: User-bound task creation with category management, priority levels, and timezone-aware deadlines.
* **Data Seeding**: Custom Django management command (`seed_data`) to generate test tasks using `Faker`.

---

## File Structure

```text
Hangarin/
├── static/                    # Global Static Assets (PWA & Media)
│   ├── js/
│   │   └── serviceworker.js   # PWA Service Worker script
│   └── img/
│       ├── icon-192.png       # PWA Application Icon (192x192)
│       └── icon-512.png       # PWA Application Icon (512x512)
├── templates/                 # Global HTML Templates (Root Level)
│   ├── account/
│   │   ├── login.html         # Custom Allauth Login Template
│   │   └── signup.html        # Custom Allauth Signup Template
│   ├── hangarin/
│   │   └── task_board.html    # Main Task Board View Template
│   └── socialaccount/
│       └── connections.html   # OAuth Account Linking Template
├── hangarin_project/          # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # App settings, PWA configuration & django-allauth
│   ├── urls.py                # Global URL routing (includes PWA routes)
│   └── wsgi.py
├── hangarin/                  # Core App Directory
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_data.py   # Fake data generation command
│   ├── migrations/            # Database migration files
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # Task, Category, and Priority models
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py                  # Django administrative script
└── requirements.txt           # Project dependencies

```

---

## Setup and Installation Guide

### 1. Clone the Repository & Set Up Virtual Environment

```bash
git clone https://github.com/QTaqua/Hangarin.git
cd Hangarin

# Create virtual environment
python -m venv hangarinenv

# Activate virtual environment
# On Windows (PowerShell):
.\hangarinenv\Scripts\Activate.ps1
# On macOS/Linux:
source hangarinenv/bin/activate

```

### 2. Install Dependencies

Install Django, `django-allauth`, `django-pwa`, `PyJWT`, `cryptography`, and `Faker`:

```bash
pip install -r requirements.txt

```

### 3. Run Migrations & Collect Static Files

Set up the SQLite database schema and assemble static assets for PWA support:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

```

### 4. Create a Superuser

Create an administrative account to access the Django admin panel (`/admin`):

```bash
python manage.py createsuperuser

```

Follow the prompts to specify a username, email, and password.

### 5. Seed Fake Data

Generate fake tasks assigned across registered database users:

```bash
python manage.py seed_data --tasks-per-user 5

```

### 6. Run the Development Server

Start the local server:

```bash
python manage.py runserver

```
## Progressive Web App (PWA) Features & Testing
### How to Install as an App

1. Open the application in Google Chrome, Microsoft Edge, or Safari on mobile.

2. Look for the Install App icon (📥) in your browser address bar (or select Add to Home Screen on mobile).

3. Click Install to launch Hangarin as a standalone desktop or mobile application.

### Testing PWA Functionality in DevTools

1. Press F12 to open Developer Tools.

2. Go to the Application tab.

3. Select Manifest to inspect app name, icons, and theme configuration.

4. Select Service Workers to verify serviceworker.js status.

5. Check the Offline box and reload the page to test offline rendering.