# Generated by Django 3.1.6 on 2021-04-26 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0010_auto_20210406_1153'),
        ('student', '0013_auto_20210418_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='placement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='placement.placement'),
        ),
    ]
