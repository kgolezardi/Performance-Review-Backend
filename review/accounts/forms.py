import django.contrib.auth.forms
from django import forms

from .models import User


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
    add_to_round = forms.BooleanField(label='Also set active round participants to these users', required=False)


class CsvRowValidationForm(forms.Form):
    employee_id = forms.IntegerField(required=True)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    manager_username = forms.CharField(required=False)
    ranking1 = forms.CharField(required=False)
    ranking2 = forms.CharField(required=False)
