from django.db import models
from user.models import CustomUser


class Category(models.Model):
    TYPE_CHOICES = (
        ("income", "Income"),
        ("outcome", "Outcome"),
    )

    image = models.ImageField(upload_to="category/", null=True, blank=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)

    def __str__(self):
        return self.get_type_display()


class Wallet(models.Model):
    TYPE_CHOICES = (
        ("cash", "Cash"),
        ("bank_card", "Bank Card"),
        ("visa", "Visa"),
    )

    CURRENCY_CHOICES = (
        ("UZS", "UZS"),
        ("USD", "USD"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=255, null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="cash"
    )
    expire_date = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to="wallets/", null=True, blank=True)

    def __str__(self):
        return self.name or self.get_type_display()


class IncomeOutcome(models.Model):
    TYPE_CHOICES = (
        ("income", "Income"),
        ("outcome", "Outcome"),
    )

    CARD_CHOICES = (
        ("cash", "Cash"),
        ("uzcard", "UzCard"),
        ("humo", "Humo"),
        ("visa", "Visa"),
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES
    )
    card_type = models.CharField(
        max_length=10,
        choices=CARD_CHOICES
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet} | {self.type} | {self.amount}"
