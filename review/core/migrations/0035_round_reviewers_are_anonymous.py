# Generated by Django 3.1.2 on 2022-06-25 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20220625_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='reviewers_are_anonymous',
            field=models.BooleanField(default=True),
        ),
    ]
