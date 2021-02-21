# Generated by Django 3.1.6 on 2021-02-21 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0010_auto_20210222_0151'),
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('domain', models.CharField(blank=True, max_length=200)),
                ('min_cgpa', models.FloatField(blank=True, default=0.0)),
                ('description', models.TextField()),
                ('min_ctc', models.FloatField()),
                ('max_ctc', models.FloatField()),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField(blank=True)),
                ('max_backlogs', models.IntegerField(blank=True, default=0)),
                ('branches_eligible', models.CharField(choices=[('CSE', 'CSE'), ('EE', 'EE'), ('ME', 'ME')], max_length=50)),
                ('job_description', models.URLField(blank=True)),
                ('salary_breakup', models.TextField(blank=True, null=True)),
                ('gender_allowed', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')], max_length=10)),
                ('extra_data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='JobRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_no', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('job_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='placement.jobprofile')),
            ],
        ),
        migrations.AddField(
            model_name='jobprofile',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_profiles', to='placement.company'),
        ),
        migrations.AddField(
            model_name='jobprofile',
            name='placement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_profiles', to='placement.placement'),
        ),
        migrations.CreateModel(
            name='JobApplicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateField(auto_now=True)),
                ('is_selected', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('job_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='placement.jobprofile')),
                ('job_round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='placement.jobround')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs_applied', to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements', to='placement.placement')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements_coordinator', to='student.student')),
            ],
            options={
                'unique_together': {('student', 'placement')},
            },
        ),
    ]
