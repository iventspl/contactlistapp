from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST

@require_http_methods(["GET", "POST"])
def api_contact_list(request):
    if request.method == 'POST':
        return HttpResponse('api post')
    elif request.method == 'GET':
        return HttpResponse('api get')

@require_http_methods(["PUT", "DELETE"])
def api_single_contact(request, pk):
    return HttpResponse('api contact')