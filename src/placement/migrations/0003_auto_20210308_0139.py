# Generated by Django 3.1.6 on 2021-03-07 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0002_auto_20210307_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
        migrations.AlterField(
            model_name='jobprofile',
            name='job_description',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]