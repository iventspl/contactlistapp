from django import forms

from .models import Contact

MAX_CSV_SIZE = 1024 * 1024

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'status']


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