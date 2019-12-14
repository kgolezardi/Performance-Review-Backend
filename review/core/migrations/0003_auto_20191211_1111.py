# Generated by Django 3.0 on 2019-12-11 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20191209_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectreview',
            name='reviewers',
            field=models.ManyToManyField(related_name='project_reviews_to_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='personreview',
            name='reviewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='personreview',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authored_person_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'NEEDS_IMPROVMENT'), (2, 'MEETS_EXPECTATIONS'), (3, 'EXCEEDS_EXPECTATIONS'), (4, 'STRONGLY_EXCEEDS_EXPECTATIONS'), (5, 'SUPERB')], null=True),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='text',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='projectreview',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'NEEDS_IMPROVMENT'), (2, 'MEETS_EXPECTATIONS'), (3, 'EXCEEDS_EXPECTATIONS'), (4, 'STRONGLY_EXCEEDS_EXPECTATIONS'), (5, 'SUPERB')], null=True),
        ),
        migrations.AlterField(
            model_name='projectreview',
            name='text',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]