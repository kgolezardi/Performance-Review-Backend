import django.contrib.auth.admin
from django.contrib import admin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'email')
    fieldsets = django.contrib.auth.admin.UserAdmin.fieldsets + (
        ('Reiew data', {'fields': ('has_started',)}),
    )
    list_filter = django.contrib.auth.admin.UserAdmin.list_filter + ('has_started',)
