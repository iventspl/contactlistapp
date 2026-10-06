from django.shortcuts import render

# Create your views here.

def home(request):

    context = {
        'page': 'home'
    }
    return render(request, 'contacts/contact_list.html', context)