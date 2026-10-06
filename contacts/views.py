from django.shortcuts import render
from .models import Contact

def contacts_list(request):
    contacts = Contact.objects.select_related('status').order_by('-created_on')
    context = {
        'contacts': contacts,
    }
    return render(request, 'contacts/contact_list.html', context)