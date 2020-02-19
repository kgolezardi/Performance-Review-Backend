from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    manager = models.ForeignKey("User", related_name='team_members', on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.IntegerField(unique=True, null=True)
    has_started = models.BooleanField(default=False, null=False, blank=False)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.username
