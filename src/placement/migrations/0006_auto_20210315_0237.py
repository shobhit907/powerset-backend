# Generated by Django 3.1.6 on 2021-03-14 21:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0005_auto_20210315_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.localdate),
        ),
    ]
