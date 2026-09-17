# Hangarin (Task Manager)

A multi-user task management web application built with Django, featuring a dark Japanese minimalist aesthetic, OAuth authentication via Google and GitHub, and seed data generation.

**Developer:** Jabriel Encarnacion

---

## Features

* **Authentication & Connections**: Complete user authentication powered by `django-allauth`, supporting Google and GitHub OAuth 2.0 integration alongside account management/linking.
* **Minimalist Japanese UI**: Customized dark-mode aesthetic utilizing deep canvas tones (`#121212`), high-contrast dark cards (`#1e1e1e`), serif headings, and crimson accents (`#e63946`).
* **Task Management**: User-bound task creation with category management, priority levels, and timezone-aware deadlines.
* **Data Seeding**: Custom Django management command (`seed_data`) to generate test tasks using `Faker`.

---

## File Structure

```text
Hangarin/
├── hangarin_project/          # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # App settings & django-allauth configuration
│   ├── urls.py                # Global URL routing
│   └── wsgi.py
├── hangarin/                  # Core App Directory
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_data.py   # Fake data generation command
│   ├── migrations/            # Database migration files
│   ├── templates/             # Custom HTML templates
│   │   ├── account/
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   └── socialaccount/
│   │       └── connections.html
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

Install Django, `django-allauth`, `PyJWT`, `cryptography`, and `Faker`:

```bash
pip install -r requirements.txt

```

### 3. Run Migrations

Set up the SQLite database schema:

```bash
python manage.py makemigrations
python manage.py migrate

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

Open your browser and navigate to `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)`
