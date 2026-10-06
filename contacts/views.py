from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Contact

def contacts_list(request):
    contacts = Contact.objects.select_related('status').order_by('-created_on')
    context = {
        'contacts': contacts,
    }
    return render(request, 'contacts/contact_list.html', context)


@require_POST
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, f"Deleted {contact} from contact list")
    return redirect('contacts:contacts_list')