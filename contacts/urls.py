from django.urls import path
from . import views

app_name = 'contacts'
urlpatterns = [
    path('', views.contacts_list, name='contacts_list'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('add/', views.contact_add, name='contact_add'),
    path('<int:pk>/edit/', views.contact_edit, name='contact_edit'),
]
