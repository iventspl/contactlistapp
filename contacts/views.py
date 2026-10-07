import logging

import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db.models import Q

from .csv_import import CsvImportError, import_contacts
from .models import Contact
from .forms import ContactForm, CsvImportForm
from .weather import get_weather_for_city

logger = logging.getLogger(__name__)

SORT_OPTIONS = {
    "last_name": ("last_name", "first_name"),
    "-last_name": ("-last_name", "-first_name"),
    "created_on": ("created_on",),
    "-created_on": ("-created_on",),
}
DEFAULT_SORT = "-created_on"


def contacts_list(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", DEFAULT_SORT)
    if sort not in SORT_OPTIONS:
        sort = DEFAULT_SORT

    contacts = Contact.objects.select_related("status").order_by(*SORT_OPTIONS[sort])
    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(city__icontains=query)
        )

    context = {
        "contacts": contacts,
        "query": query,
        "sort": sort,
    }
    return render(request, "contacts/contact_list.html", context)

@require_POST
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.warning(request, f"Deleted {contact} from contact list!")
    return redirect('contacts:contacts_list')


@require_http_methods(['POST', 'GET'])
def contact_add(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"Added {contact} to contact list")
            return redirect('contacts:contacts_list')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'page': 'Add',
    }
    return render(request, 'contacts/contact_form.html', context)


@require_http_methods(['POST', 'GET'])
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"Updated {contact} succesfully")
            return redirect('contacts:contacts_list')
    else:
        form = ContactForm(instance=contact)

    context = {
        'form': form,
        'page': 'Edit',
    }
    return render(request, 'contacts/contact_form.html', context)


@require_GET
def city_weather(request):
    """Return current weather for the 'city' query parameter as JSON"""
    city = request.GET.get("city", "").strip()
    if not city:
        return JsonResponse({"error": "Missing 'city' parameter."}, status=400)

    try:
        weather = get_weather_for_city(city)
    except requests.RequestException:
        logger.exception("Weather lookup failed for city %r", city)
        return JsonResponse({"error": "Weather service unavailable."}, status=502)

    if weather is None:
        return JsonResponse({"error": "City not found."}, status=404)

    return JsonResponse(weather)


@require_http_methods(['POST', 'GET'])
def contact_import(request):
    if request.method == 'POST':
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                imported_count, errors = import_contacts(form.cleaned_data['file'])
            except CsvImportError as error:
                form.add_error('file', str(error))
            else:
                if not errors:
                    messages.success(request, f"Imported {imported_count} contacts.")
                    return redirect('contacts:contacts_list')
                context = {
                    'form': CsvImportForm(),
                    'imported_count': imported_count,
                    'errors': errors,
                }
                return render(request, 'contacts/contact_import.html', context)
    else:
        form = CsvImportForm()
    return render(request, 'contacts/contact_import.html', {'form': form})
