import re

from django import forms
from django.forms import widgets

from main.models import LoanApplication


class LoanAppForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    phone_number = forms.CharField(max_length=10)
    comment = forms.CharField(max_length=250, required=False)
    date_application = forms.DateTimeField()

    class Meta:
        model = LoanApplication
        exclude = ['client_fk', 'date_application']

    def clean(self):
        cleaned_data = super().clean()

        if not re.match(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', str(cleaned_data['phone_number'])):
            self.add_error('phone_number',
                           'Number phone is not correct, please enter number for mask - 0000000000')

        return cleaned_data
