import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from contacts.forms import ContactForm
from contacts.models import Contact


def serialize_contact(contact):
    """Return contact field as JSON-format"""
    return {
        "id": contact.id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "city": contact.city,
        "status": contact.status.status,
        "created_on": contact.created_on,
    }


def parse_json_body(request):
    """Return the request body as a dict, or None if it is not a valid JSON object."""
    try:
        data = json.loads(request.body)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_contact_list(request):
    if request.method == "GET":
        contacts = Contact.objects.select_related("status").order_by("-created_on")
        return JsonResponse([serialize_contact(contact) for contact in contacts], safe=False)
    
    data = parse_json_body(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    form = ContactForm(data)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    contact = form.save()
    return JsonResponse(serialize_contact(contact), status=201)


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def api_single_contact(request, pk):
    try:
        contact = Contact.objects.select_related("status").get(pk=pk)
    except Contact.DoesNotExist:
        return JsonResponse({"error": "Contact not found."}, status=404)

    if request.method == "DELETE":
        contact.delete()
        return HttpResponse(status=204)

    data = parse_json_body(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    form = ContactForm(data, instance=contact)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

    contact = form.save()
    return JsonResponse(serialize_contact(contact))
