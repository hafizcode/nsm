# Generated by Django 5.2 on 2025-04-18 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_uploadedfile_download_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='download_count',
        ),
    ]
