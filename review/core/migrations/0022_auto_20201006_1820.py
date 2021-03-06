# Generated by Django 3.1.2 on 2020-10-06 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_set_round_foreign_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerpersonreview',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.round'),
        ),
        migrations.AlterField(
            model_name='personreview',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.round'),
        ),
        migrations.AlterField(
            model_name='projectreview',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.round'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='active_round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.round'),
        ),
    ]
