# Generated by Django 3.1.6 on 2021-04-06 06:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0009_jobprofile_number_of_rounds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplicant',
            name='job_round',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]