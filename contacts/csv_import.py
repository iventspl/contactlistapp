import csv
import io

from .forms import ContactForm
from .models import ContactStatus

REQUIRED_COLUMNS = ["first_name", "last_name", "phone_number", "email", "city", "status"]


class CsvImportError(Exception):
    """Raised when the file as cannot be processed (encoding, missing columns)"""


def import_contacts(file):
    """Create contacts from an uploaded CSV file.

    Valid rows are saved and invalid rows are skipped.
    Returns (imported_count, errors), where errors is a list of (line_number, message).
    """
    reader = _read_csv(file)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
    if missing_columns:
        raise CsvImportError(f"Missing columns: {', '.join(missing_columns)}.")

    # One query for all statuses instead of one per row.
    statuses = {status.status.casefold(): status.pk for status in ContactStatus.objects.all()}

    imported_count = 0
    errors = []
    for row in reader:
        data = {column: (row[column] or "").strip() for column in REQUIRED_COLUMNS}

        status_name = data["status"]
        data["status"] = statuses.get(status_name.casefold())
        if data["status"] is None:
            errors.append((reader.line_num, f"Unknown status '{status_name}'."))
            continue

        form = ContactForm(data)
        if not form.is_valid():
            errors.append((reader.line_num, _format_form_errors(form)))
            continue

        form.save()
        imported_count += 1

    return imported_count, errors


def _read_csv(file):
    try:
        text = file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        raise CsvImportError("The file must be UTF-8 encoded (in Excel: Save as 'CSV UTF-8').")

    try:
        dialect = csv.Sniffer().sniff(text[:2048], delimiters=",;")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    reader.fieldnames = [name.strip() for name in reader.fieldnames or []]
    return reader


def _format_form_errors(form):
    return "; ".join(f"{field}: {' '.join(messages)}" for field, messages in form.errors.items())
