from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('uz', 'Uzbek'),
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    address = models.CharField(max_length=100, null=True, blank=True)

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.phone_number:
            phone = self.phone_number.strip()

            if len(phone) == 9 and phone.isdigit():
                phone = f"+998{phone}"

            elif len(phone) == 12 and phone.isdigit():
                phone = f"+{phone}"

            elif phone.startswith("+") and phone[1:].isdigit():
                pass

            else:
                raise ValueError("Invalid phone number")

            self.phone_number = phone

        super().save(*args, **kwargs)