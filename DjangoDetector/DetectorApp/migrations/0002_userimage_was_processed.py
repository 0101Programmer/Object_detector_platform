# Generated by Django 5.0.4 on 2024-10-20 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DetectorApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='was_processed',
            field=models.BooleanField(default=False),
        ),
    ]
