from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.IntegerField(blank=True,null=True)
    avatar = models.ImageField(upload_to='avatars/',default='avatars/default.png')
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
