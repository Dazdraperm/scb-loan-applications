import re

from django import forms
from main.models import LoanApplication


class LoanAppForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    comment = forms.CharField(max_length=250, required=False)
    date_application = forms.DateTimeField()

    class Meta:
        model = LoanApplication
        exclude = ['id', 'client_fk', 'date_application']

    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     if not re.match(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', str(self.client_fk)):
    #         self.add_error('client_phone_number',
    #                        'Number phone is not correct, please enter number for mask - 0000000000')
    #
    #     return cleaned_data
