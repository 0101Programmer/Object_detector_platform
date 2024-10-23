from django.db import models


# Create your models here.

class MyAppUser(models.Model):
    name = models.TextField(default=None)
    user_password = models.TextField(default=None)

    def __str__(self):
        return self.name


class CurrentUser(models.Model):
    current_user = models.TextField(default='Вход не выполнен')

    def __repr__(self):
        return self.current_user

    def __str__(self):
        return self.current_user


class UserImage(models.Model):
    enter_user_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users_photos/', null=True)
    was_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.enter_user_name


class ProcessedUserImage(models.Model):
    # processed_image = models.ImageField(upload_to='processed_photos/', null=True)
    processed_image = models.ImageField(upload_to='', null=True)
    image_user_name = models.CharField(max_length=50)
    object_type = models.CharField(max_length=100)
    confidence = models.FloatField()
    location = models.CharField(max_length=255)



