import csv
from io import StringIO

import django.contrib.auth.admin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from accounts.interactors import add_user
from .forms import UserCreationForm, UserChangeForm, CsvRowValidationForm, CsvImportForm
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
    change_list_template = 'accounts/change_list_with_import.html'

    def get_urls(self):
        my_urls = [path('import-users', self.admin_site.admin_view(self.add_users))]
        return my_urls + super().get_urls()

    def add_users(self, request):
        if request.method == "POST":
            csv_content = StringIO(request.FILES["csv_file"].read().decode('utf-8'))
            reader = csv.DictReader(csv_content, delimiter=',')
            successful, unsuccessful = 0, 0
            for row in reader:
                success = False
                if CsvRowValidationForm(row).is_valid():
                    username = row['email'].split('@')[0]
                    success = add_user(username=username, **row)
                if success:
                    successful += 1
                else:
                    unsuccessful += 1

            level = messages.SUCCESS if unsuccessful == 0 else messages.WARNING
            self.message_user(request, "Added %d users successfully, and %d row(s) had error."
                              % (successful, unsuccessful), level)
            return redirect('.')

        form = CsvImportForm()
        context = {
            'title': 'Import users',
            'form': form,
            'opts': self.model._meta,
            **self.admin_site.each_context(request)
        }
        return TemplateResponse(request, 'accounts/import_users.html', context)

