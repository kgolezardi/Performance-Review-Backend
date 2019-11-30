from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    manager = models.ForeignKey("User", related_name='team_members', on_delete=models.SET_NULL, null=True)
    employee_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.username
