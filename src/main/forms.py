import re

from django import forms
from django.forms import widgets

from main.models import LoanApplication

date_errors = {
    'invalid': 'mask must have is ( year-month-day hours:minute:second ) example: 2021-06-06 23:45:13'
}


class LoanAppForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    phone_number = forms.CharField(max_length=10)
    comment = forms.CharField(max_length=250, required=False)
    date_application = forms.DateTimeField(error_messages=date_errors)

    class Meta:
        model = LoanApplication
        exclude = ['client_fk', 'date_application']

    def clean(self):
        cleaned_data = super().clean()

        if not re.match(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', str(cleaned_data['phone_number'])):
            self.add_error('phone_number',
                           'Number phone is not correct, please enter number for mask - 0000000000')

        return cleaned_data


class AuthForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class RegistrationForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()
    password2 = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data
