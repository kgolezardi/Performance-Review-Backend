import django.contrib.auth.forms

from .models import User


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
