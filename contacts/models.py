from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^\+?\d{9,15}$",
    message="Enter 9 to 15 digits, optionally starting with +",
)

class ContactStatus(models.Model):
    status = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.status}"


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16, unique=True, validators=[phone_validator])
    email = models.EmailField(max_length=255, unique=True)
    city = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT, related_name='contacts')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
