# Contact List

A Django web application for managing contacts, built as a recruitment task
for the Junior Fullstack Developer position.

## Features

- Contact list with search (name, email, phone, city) and sorting (last name, date added)
- Adding, editing and deleting contacts (with a confirmation dialog)
- Import of contacts from a CSV file with a per-row error report
- Current weather (temperature, humidity, wind speed) shown next to each contact's city
- REST API for listing, creating, updating and deleting contacts
- Client-side (JavaScript) and server-side form validation
- Contact statuses managed in the database (admin panel)
- Responsive interface built with Bootstrap 5

## Tech stack

- Python 3.12, Django 6.1, SQLite
- Bootstrap 5 (CDN), vanilla JavaScript
- django-crispy-forms + crispy-bootstrap5 (form rendering)
- requests (weather APIs), python-dotenv (configuration)
- django-debug-toolbar (development only, enabled when `DEBUG=True`)

## Installation

**Requirements:** Python 3.12+

1. Clone the repository:

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

4. Create the `.env` file and set a secret key:

   ```bash
   cp .env.example .env
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Paste the generated key as `SECRET_KEY` in `.env`:

   ```
   SECRET_KEY=<generated key>
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Apply migrations and create an admin account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open http://127.0.0.1:8000/admin/, log in and add contact statuses,
   e.g. `nowy`, `w trakcie`, `zagubiony`, `nieaktualny`.
   A contact cannot be created without a status.

## Usage

| URL | Description |
|---|---|
| `/` | Contact list: search, sorting, weather, edit and delete actions |
| `/add/` | Add a contact |
| `/<id>/edit/` | Edit a contact |
| `/import/` | Import contacts from a CSV file |
| `/weather/?city=<name>` | Current weather for a city as JSON (used by the contact list) |
| `/admin/` | Admin panel (contacts and statuses) |

### CSV import

The first row must contain the column names:

```csv
first_name,last_name,phone_number,email,city,status
Jan,Kowalski,+48123456789,jan.kowalski@example.com,Warszawa,nowy
```

- Values can be separated by commas or semicolons (Excel in Polish locale uses semicolons).
- The file must be UTF-8 encoded (in Excel: *Save as → CSV UTF-8*), max 1 MB.
- `status` is the name of an existing status (case-insensitive).
- Valid rows are imported; invalid rows are skipped and listed with their line number and the reason.

## REST API

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `GET` | `/api/contacts/` | List of contacts (id, first name, last name, city, status, date added) | `200` |
| `POST` | `/api/contacts/` | Create a contact | `201` |
| `PUT` | `/api/contacts/<id>/` | Update a contact (all fields required) | `200` |
| `DELETE` | `/api/contacts/<id>/` | Delete a contact | `204` |

Request bodies are JSON. `status` is sent as the status **id** and returned as the status **name**.
The status id can be found in the admin panel (e.g. `/admin/contacts/contactstatus/1/change/`);
the first status created after installation has id `1`.

Errors are returned as JSON with status `400` (invalid JSON or validation errors) or `404` (contact not found).
An unsupported HTTP method returns `405`.

```bash
# List
curl http://127.0.0.1:8000/api/contacts/

# Create
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jan", "last_name": "Kowalski", "phone_number": "+48123456789",
       "email": "jan@example.com", "city": "Kraków", "status": 1}'

# Update
curl -X PUT http://127.0.0.1:8000/api/contacts/1/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jan", "last_name": "Nowak", "phone_number": "+48123456789",
       "email": "jan@example.com", "city": "Gdańsk", "status": 1}'

# Delete
curl -X DELETE http://127.0.0.1:8000/api/contacts/1/
```

## Project structure

| Path | Responsibility |
|---|---|
| `contacts/models.py` | `Contact` and `ContactStatus` models, phone number validator |
| `contacts/views.py` | Web interface views and the weather JSON endpoint |
| `contacts/forms.py` | `ContactForm` (shared by the UI, the API and the CSV import), CSV upload form |
| `contacts/weather.py` | Geocoding (Nominatim) and weather (Open-Meteo) with caching |
| `contacts/csv_import.py` | CSV parsing and row-by-row import |
| `contacts/static/contacts/js/` | Delete confirmation, weather loading, form validation |
| `api/views.py` | REST API endpoints |

## Design decisions

### One validation path for every entry point

The web form, the REST API and the CSV import all validate data with the same `ContactForm`.
Required fields, email format, phone format and uniqueness are defined once and behave
the same everywhere.

### Validation

- **Client side:** HTML5 constraints (`required`, `type="email"`, `pattern`) rendered by Django,
  displayed in Bootstrap style by `form-validation.js`. Without JavaScript the browser's
  native validation still works.
- **Server side:** the phone number must have 9–15 digits, optionally starting with `+` (model validator).
  Spaces, dashes and brackets are removed before validation, so `+48 123 456 789`
  and `+48123456789` are treated as the same number.
- Phone numbers and email addresses are unique.

### Weather and limiting API requests

- The contact list renders immediately; weather is loaded afterwards via AJAX from an internal
  endpoint (`/weather/?city=...`), so a slow or unavailable weather service never blocks the page.
- Each unique city is requested only once per page, and the requests are sent sequentially
  to avoid bursts of calls to the external APIs.
- Results are cached on the server (Django local memory cache):
  - city coordinates (Nominatim) for 30 days, since they practically never change,
  - weather (Open-Meteo) for 30 minutes,
  - "city not found" results are cached too, so a typo in a city does not trigger repeated lookups.
- API failures are not cached, so the next request retries. They are logged on the server
  and shown in the UI as "Unavailable".

### Contact statuses

- Statuses are a separate `ContactStatus` model and `Contact.status` is a `ForeignKey` to it,
  so statuses can be added or renamed in the admin panel or directly in the database.
- Statuses are reference data and cannot be deleted: `on_delete=PROTECT` blocks deleting a status
  in use, and the delete action is disabled for statuses in the admin panel.

### Configuration

- `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` are read from a `.env` file excluded from the repository.

## Known limitations

- The REST API has no authentication, so CSRF protection is disabled for its endpoints.
- The local memory cache is per process and is cleared on restart; in production it would be replaced by Redis.
- SQLite's case-insensitive search works only for ASCII letters (e.g. `ł` vs `Ł`); PostgreSQL does not have this limitation.

## Additional tasks

- **Caching:** weather and geocoding results are cached (see *Weather and limiting API requests*).
