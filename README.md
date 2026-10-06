# Contact List

A simple Django web application for managing contacts, built as a recruitment task
for the Junior Fullstack Developer position.

## Tech stack

- Python 3.12
- Django 6.1
- SQLite
- python-dotenv (configuration via environment variables)

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/iventspl/contactlistapp.git
   cd contactlistapp
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the `.env` file from the template:

   ```bash
   cp .env.example .env
   ```

   Generate a secret key and paste it as the `SECRET_KEY` value in `.env`:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Example `.env`:

   ```
   SECRET_KEY=<generated key>
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create an admin account:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Log in to the admin panel at http://127.0.0.1:8000/admin/ and add contact statuses
   (e.g. "Nowy", "W trakcie", "Zagubiony", "Nieaktualny"). A contact cannot be created without a status!.

## Usage

| URL | Description |
|---|---|
| `/` | Contact list |
| `/admin/` | Django admin panel (contacts and statuses) |
| `/api/contacts/` | REST API: list (`GET`), create (`POST`) |
| `/api/contacts/<id>/` | REST API: update (`PUT`), delete (`DELETE`) |

## Project structure

| App | Responsibility |
|---|---|
| `contacts` | Models, admin and web interface for contacts |
| `api` | REST API endpoints |
| `accounts` | User authentication |

## Design decisions

### Contact statuses

- Statuses are stored in a separate `ContactStatus` model, and `Contact.status` is a `ForeignKey` to it.
  Statuses can be added or renamed in the admin panel or directly in the database, without code changes.
- Statuses are treated as reference data and **cannot be deleted**:
  - `on_delete=PROTECT` blocks deleting a status that is assigned to any contact,
  - the delete action is disabled for statuses in the admin panel,
  - at the database level, the foreign key constraint blocks deleting a status that is in use.
- Every contact must have a status (the field is not nullable).

### Data integrity

- Phone numbers and email addresses are unique (`unique=True`), as required by the task.

### Configuration

- Secrets and environment-specific settings (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) are read from a `.env` file,
  which is excluded from the repository. `.env.example` documents the required variables.
