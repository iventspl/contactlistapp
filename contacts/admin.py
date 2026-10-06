from django.contrib import admin
from .models import Contact, ContactStatus

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'created_on', 'status']
    list_filter = ['last_name', 'city', 'status']
    search_fields = ['first_name', 'last_name', 'phone_number', 'email', 'city']


@admin.register(ContactStatus)
class ContactStatusAdmin(admin.ModelAdmin):
    list_display = ['status']

    def has_delete_permission(self, request, obj=None):
        # Statuses are reference data. Deleting them is not allowed (see README)
        return False