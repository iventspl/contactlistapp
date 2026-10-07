import re

from django import forms

from .models import Contact

MAX_CSV_SIZE = 1024 * 1024
PHONE_SEPARATORS = re.compile(r"[\s\-()]")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'status']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'type': 'tel',
                'inputmode': 'tel',
                'pattern': r'\+?\d{9,15}',
                'placeholder': '+48123456789',
                'data-pattern-message': 'Enter 9 to 15 digits, optionally starting with +',
            }),
        }

        def clean_phone_number(self):
            """Remove spaces, dashes and brackets so equal numbers are stored the same way"""
            return PHONE_SEPARATORS.sub('', self.cleaned_data['phone_number'])


class CsvImportForm(forms.Form):
    file = forms.FileField(label="CSV file",
                           widget=forms.ClearableFileInput(attrs={"accept": ".csv"}),
                           )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a .csv file.")
        if file.size > MAX_CSV_SIZE:
            raise forms.ValidationError("The file is too large (max 1 MB).")
        return file