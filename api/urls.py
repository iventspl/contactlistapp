from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('api/contacts/', views.api_contact_list, name='api_contact_list'),
    path('api/contacts/<int:pk>/', views.api_single_contact, name='api_single_contact'),
]
