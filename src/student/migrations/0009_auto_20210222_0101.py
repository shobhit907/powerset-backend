# Generated by Django 3.1.6 on 2021-02-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20210221_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('logo', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='awardandrecognition',
            old_name='Issuer',
            new_name='issuer',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='InstituteName',
            new_name='instituteName',
        ),
        migrations.RenameField(
            model_name='patent',
            old_name='Number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='patent',
            old_name='Office',
            new_name='office',
        ),
        migrations.RenameField(
            model_name='patent',
            old_name='Status',
            new_name='status',
        ),
    ]
