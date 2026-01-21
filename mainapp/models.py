from django.db import models
from django.conf import settings
from decimal import Decimal


# Create your models here.
class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )
    title = models.CharField(max_length=32)
    type_p = models.CharField(max_length=8, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title


class Wallet(models.Model):
    TYPE_CHOICES = (
        ('cash', 'CASH'),
        ('card', 'Bank card'),
        ('other', 'OTHER'),
    )
    CURRENCY_CHOICES=( ("UZS", ("UZS")),
        ("USD", ("USD")),)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default='other')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    created = models.DateTimeField(auto_now_add=True)
    currency=models.CharField(max_length=3,choices=CURRENCY_CHOICES)


    def __str__(self):
        return self.title


class IncomeOutcome(models.Model):
    TYPE_CHOICES = [
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallets')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} - {self.wallet.title} - {self.amount}"
