import django.contrib.auth.admin
from django.contrib import admin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email']
