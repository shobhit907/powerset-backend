# Generated by Django 3.1.6 on 2021-03-07 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0002_auto_20210307_1345'),
        ('student', '0004_auto_20210307_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='placement.institute'),
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
    ]