from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from .models import Contact
from .forms import ContactForm

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
