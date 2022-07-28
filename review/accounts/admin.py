import csv
from io import StringIO

import django.contrib.auth.admin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from accounts.interactors.user import add_user, set_user_manager, set_user_rankings
from core.interactors.round import add_users_to_active_round
from .forms import UserCreationForm, UserChangeForm, CsvRowValidationForm, CsvImportForm
from .models import User


@admin.register(User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'name', 'manager')
    fieldsets = django.contrib.auth.admin.UserAdmin.fieldsets + (
        ('Review data', {'fields': ('employee_id', 'manager', 'avatar_url', 'ranking1', 'ranking2', 'is_hr')}),
    )
    change_list_template = 'accounts/change_list_with_import.html'

    def get_urls(self):
        my_urls = [path('import-users', self.admin_site.admin_view(self.import_users))]
        return my_urls + super().get_urls()

    def import_users(self, request):
        if request.method == "POST":
            add_to_round = 'add_to_round' in request.POST and request.POST['add_to_round'] == 'on'
            csv_content = StringIO(request.FILES["csv_file"].read().decode('utf-8'))
            reader = csv.DictReader(csv_content, delimiter=',')
            users_managers = []
            rankings = []
            usernames = []
            created, updated, unsuccessful = 0, 0, 0

            for row in reader:
                status = -1
                if CsvRowValidationForm(row).is_valid():
                    username = row['email'].split('@')[0]
                    manager_username = row.pop('manager_username', None)
                    ranking1 = row.pop('ranking1', None)
                    ranking2 = row.pop('ranking2', None)
                    status = add_user(username=username, **row)
                    if manager_username:
                        users_managers.append((username, manager_username))
                    if ranking1 or ranking2:
                        rankings.append((username, ranking1, ranking2))
                    usernames.append(username)
                if status == 0:
                    updated += 1
                elif status == 1:
                    created += 1
                else:
                    unsuccessful += 1

            for username, manager_username in users_managers:
                success = set_user_manager(username, manager_username)
                if not success:
                    unsuccessful += 1

            for username, ranking1, ranking2 in rankings:
                success = set_user_rankings(username, ranking1, ranking2)
                if not success:
                    unsuccessful += 1

            if add_to_round:
                add_users_to_active_round(usernames)

            level = messages.SUCCESS if unsuccessful == 0 else messages.WARNING
            self.message_user(request, "%d users were created, %d users got updated, and %d errors detected."
                              % (created, updated, unsuccessful), level)
            return redirect('.')

        form = CsvImportForm()
        context = {
            'title': 'Import users',
            'form': form,
            'opts': self.model._meta,
            **self.admin_site.each_context(request)
        }
        return TemplateResponse(request, 'accounts/import_users.html', context)
