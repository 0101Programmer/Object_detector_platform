# Generated by Django 5.0.4 on 2024-10-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='MyAppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None)),
                ('user_password', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedUserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processed_image', models.ImageField(null=True, upload_to='processed_photos/')),
                ('image_user_name', models.CharField(max_length=50)),
                ('object_type', models.CharField(max_length=100)),
                ('confidence', models.FloatField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_user_name', models.CharField(max_length=50)),
                ('image', models.ImageField(null=True, upload_to='users_photos/')),
            ],
        ),
    ]
