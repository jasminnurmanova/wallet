from django.contrib import admin
from .models import Wallet, IncomeOutcome, Category

admin.site.register([Wallet, IncomeOutcome, Category])
# Register your models here.