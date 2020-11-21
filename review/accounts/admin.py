import csv
from io import StringIO

import django.contrib.auth.admin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from accounts.interactors import add_user, get_user_progress, set_user_manager
from core.enums import Phase
from core.interactors.project_review import get_users_to_review
from core.interactors.settings import is_at_phase
from .forms import UserCreationForm, UserChangeForm, CsvRowValidationForm, CsvImportForm
from .models import User


@admin.register(User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'get_name', 'get_progess', 'manager', 'get_users_to_review')
    fieldsets = django.contrib.auth.admin.UserAdmin.fieldsets + (
        ('Review data', {'fields': ('employee_id', 'manager', 'avatar_url')}),
    )
    change_list_template = 'accounts/change_list_with_import.html'

    def get_urls(self):
        my_urls = [path('import-users', self.admin_site.admin_view(self.import_users))]
        return my_urls + super().get_urls()

    def import_users(self, request):
        if request.method == "POST":
            csv_content = StringIO(request.FILES["csv_file"].read().decode('utf-8'))
            reader = csv.DictReader(csv_content, delimiter=',')
            users_managers = []
            created, updated, unsuccessful = 0, 0, 0

            for row in reader:
                status = -1
                if CsvRowValidationForm(row).is_valid():
                    username = row['email'].split('@')[0]
                    manager_username = row.pop('manager_username', None)
                    status = add_user(username=username, **row)
                    if manager_username:
                        users_managers.append((username, manager_username))
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

            level = messages.SUCCESS if unsuccessful == 0 else messages.WARNING
            self.message_user(request, "%d users were created, %d users got updated, and %d row(s) had error."
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

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    get_name.short_description = 'Name'

    def get_progess(self, obj):
        if is_at_phase(Phase.SELF_REVIEW):
            progress = get_user_progress(obj)
            res = 'Criteria: %d%% - SW: %d%% - P: %s' % (progress['performance_competencies'],
                                                         progress['dominant_characteristics'],
                                                         list(map(int, progress['projects'])))
            return res
        return ''

    get_progess.short_description = 'Progress'

    def get_users_to_review(self, obj):
        return ', '.join(get_users_to_review(obj).values_list('username', flat=True))

    get_users_to_review.short_description = 'Users to review'
