from django.shortcuts import render
from .models import ContactStatus, Contact

# Create your views here.

def contacts_list(request):
    contacts = Contact.objects.all().order_by('-created_on')
    context = {
        'page': 'contacts',
        'contacts': contacts,
    }
    return render(request, 'contacts/contact_list.html', context)